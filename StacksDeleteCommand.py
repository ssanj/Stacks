import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksLoaderCommand import StacksLoaderCommand, SelectedStackName
from Stacks.components.FileUtils import SaveError, save_stack_file
from Stacks.components.Files import StackFileName
from Stacks.components.ResultTypes import Either
from logging import Logger

class StacksDeleteCommand(StacksLoaderCommand):

  def loader_message(self) -> str:
    return "Which stack would you like to delete?"


  def on_stack_name_selected(self, window: sublime.Window, logger: Logger, stack_file: StackFileName, loaded_stacks: Dict[str, Any], selected_stack_name: SelectedStackName) -> None:
    stack_to_delete = selected_stack_name.value

    loaded_stacks.pop(stack_to_delete, None)
    updated_stack_content = json.dumps(loaded_stacks)

    save_result: Either[SaveError, None] = save_stack_file(stack_file, updated_stack_content)
    if save_result.has_value():
      # get the currently loaded stack name
      current_stack_name = window.settings().get(_loaded_stack_name_settings_key)

      # if it matches the deleted stack name, then remove it from settings
      if current_stack_name and current_stack_name == stack_to_delete:
        window.settings().erase(_loaded_stack_name_settings_key)

      sublime.message_dialog(f"Deleted {stack_to_delete}")
    else:
      error: SaveError = save_result.error()
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(error.value)}")

