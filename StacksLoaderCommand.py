import sublime
from Stacks.StacksCommand import StacksCommand
from abc import abstractmethod
from typing import NamedTuple, Optional, List, Any, Dict
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
