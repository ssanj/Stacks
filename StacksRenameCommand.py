import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksLoaderCommand import StacksLoaderCommand, SelectedStackName
from Stacks.components.FileUtils import save_stack_file
from Stacks.components.FileUtils import SaveError
from Stacks.components.Files import StackFileName
from Stacks.components.ResultTypes import Either
from logging import Logger

class StacksRenameCommand(StacksLoaderCommand):

  def loader_message(self) -> str:
    return "Which stack would you like to rename?"


  def on_stack_name_selected(self, window: sublime.Window, logger: Logger, stack_file: StackFileName, loaded_stacks: Dict[str, Any], selected_stack_name: SelectedStackName) -> None:
    window.show_input_panel(
      caption = "Stack name",
      on_done = lambda new_stack_name: self.on_stack_rename(stack_file, selected_stack_name, loaded_stacks, window, new_stack_name),
      initial_text = selected_stack_name.value,
      on_change = None,
      on_cancel = None
    )

  def on_stack_rename(self, stack_file: StackFileName, selected_stack_name: SelectedStackName, loaded_stacks: Dict[str, Any], window: sublime.Window, new_stack_name: str) -> None:
    old_stack_name = selected_stack_name.value
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

