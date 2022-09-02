import sublime
from Stacks.StacksCommand import StacksCommand
from abc import abstractmethod
from typing import NamedTuple, Optional, List, Any, Dict, Tuple
from Stacks.components.FileUtils import LoadError, load_stack_file
from Stacks.components.ResultTypes import Either, RightEither, LeftEither
from Stacks.components.Files import StackFileName
from logging import Logger

class SelectedStackName(NamedTuple):
  value: str

class StacksLoaderCommand(StacksCommand):

  def on_run(self, window: sublime.Window, logger: Logger, stack_file: StackFileName) -> None:
    load_result: Either[LoadError, Dict[str, Any]] = load_stack_file(stack_file)

    if load_result.has_value():
      loaded_stacks = load_result.value()
      items: List[str] = [key for key in loaded_stacks.keys()]

      window.show_quick_panel(
        items = items,
        placeholder = self.loader_message(),
        on_highlight = lambda index: self.on_stack_highlight(window, logger, stack_file, loaded_stacks, items, index),
        on_select = lambda index: self.on_stack_loaded(window, logger, stack_file, loaded_stacks, items, index)
      )
    else:
      error: LoadError = load_result.error()

      if error == LoadError.STACK_FILE_NOT_FOUND:
        sublime.message_dialog(f"Could not find saved file:\n{stack_file}.\nPlease try saving a stack first.")
      elif error == LoadError.COULD_NOT_DECODE_STACK_FILE:
        sublime.message_dialog(f"Could not decode {stack_file}.\nConsider deleting it and resaving it or make it a valid json file.")
      else:
        sublime.message_dialog(f"An unexpected error occurred: {error}")

  def on_stack_highlight(self, window: sublime.Window, logger: Logger, stack_file: StackFileName, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_name_index: int) -> None:
    if stack_name_index < 0 or stack_name_index > len(stack_names):
      return

    selected_stack_name = stack_names[stack_name_index]
    stack = loaded_stacks.get(selected_stack_name)
    if not stack:
      return

    stack_to_preview: Dict[str, Any] = stack

    group_names: List[str] = [key for key in stack_to_preview.keys() if key.startswith("group")]

    group_files: List[Tuple[str, List[str]]] = [(g, stack_to_preview[g]) for g in group_names]

    view = window.active_view()
    if view:
      content = f"<h2>{selected_stack_name}</h2>"
      for gf in group_files:
        group_str: str = gf[0]
        files: List[str] = gf[1]
        files_str: str = "<br/>".join(files)
        content = f"{content}<br/>{group_str}:<br/>{files_str}"

      layout_extent: Tuple[float, float] = view.viewport_extent()
      max_width  = int(layout_extent[0])
      max_height = int(layout_extent[1])
      location = self.get_centre_point(view)

      view.show_popup(content, location = location, max_width = max_width, max_height = max_height)


  def get_centre_point(self, view: sublime.View) -> int:
    # copied from https://forum.sublimetext.com/t/move-cursor-to-top-middle-bottom-of-visible-lines/4586
    screenful = view.visible_region()

    col = view.rowcol(view.sel()[0].begin())[1]
    row_a = view.rowcol(screenful.a)[0]
    row_b = view.rowcol(screenful.b)[0]

    middle_row = int((row_a + row_b) / 2)
    location = view.text_point(middle_row, col)

    return location


  def on_stack_loaded(self, window: sublime.Window, logger: Logger, stack_file: StackFileName, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_name_index: int) -> None:
    if stack_name_index < 0 or stack_name_index > len(stack_names):
      return

    selected_stack_name = SelectedStackName(stack_names[stack_name_index])
    self.on_stack_name_selected(window, logger, stack_file, loaded_stacks, selected_stack_name)

  @abstractmethod
  def on_stack_name_selected(self, window: sublime.Window, logger: Logger, stack_file: StackFileName, loaded_stacks: Dict[str, Any], selected_stack_name: SelectedStackName) -> None:
    pass

  @abstractmethod
  def loader_message(self) -> str:
    pass
