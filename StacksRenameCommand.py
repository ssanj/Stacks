import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksLoaderCommand import StacksLoaderCommand
from Stacks.components.FileUtils import save_stack_file
from Stacks.components.FileUtils import SaveError
from Stacks.components.Files import StackFileName
from Stacks.components.ResultTypes import Either

class StacksRenameCommand(StacksLoaderCommand):

  def loader_message(self) -> str:
    return "Which stack would you like to rename?"


  def on_stack_loaded(self, stack_file: StackFileName, window: sublime.Window, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_name_index: int) -> None:
    if stack_name_index < 0 or stack_name_index > len(stack_names):
      return

    stack_to_rename = stack_names[stack_name_index]

    window.show_input_panel(
      caption = "Stack name",
      on_done = lambda new_stack_name: self.on_stack_rename(stack_file, stack_to_rename, loaded_stacks, window, new_stack_name),
      initial_text = "",
      on_change = None,
      on_cancel = None
    )

  def on_stack_rename(self, stack_file: StackFileName, old_stack_name: str, loaded_stacks: Dict[str, Any], window: sublime.Window, new_stack_name: str) -> None:

    stack_content = loaded_stacks.pop(old_stack_name, None)

    # we found the existing stack for the old name
    if stack_content:
      loaded_stacks.update({new_stack_name : stack_content})
    else:
      # Add an empty stack if things have gone wrong
      loaded_stacks.update({new_stack_name : {}})

    updated_stack_content = json.dumps(loaded_stacks)

    save_result: Either[SaveError, None] = save_stack_file(stack_file, updated_stack_content)
    if save_result.has_value():
      # get the currently loaded stack name
      current_stack_name = window.settings().get(_loaded_stack_name_settings_key)

      # if it matches the old stack name, then rename it in the settings
      if current_stack_name and current_stack_name == old_stack_name:
        window.settings().update({ _loaded_stack_name_settings_key: new_stack_name})
    else:
      error: SaveError = save_result.error()
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(error.value)}")

