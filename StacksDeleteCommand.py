import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksCommand import StacksCommand

class StacksDeleteCommand(StacksCommand):

  def on_run(self, window: sublime.Window, stack_file: str):
    if os.path.exists(stack_file):
      with open(stack_file, "r") as file:
        try:
          loaded_stacks: Dict[str, Any] = json.loads(file.read())
        except json.decoder.JSONDecodeError:
          sublime.message_dialog(f"Could not decode {stack_file}.\nConsider deleting it and resaving it or make it a valid json file.")
          return

        items: List[str] = [key for key in loaded_stacks.keys()]

        window.show_quick_panel(
          items = items,
          placeholder = "Which stack would you like to delete?",
          on_select = lambda index: self.on_stack_delete(stack_file, window, loaded_stacks, items, index)
        )
    else:
      sublime.message_dialog(f"Could not find saved file:\n{stack_file}.\nPlease try saving a stack first.")

  def on_stack_delete(self, stack_file: str, window: sublime.Window, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_index: int) -> None:
    if stack_index < 0 or stack_index > len(stack_names):
      return

    stack_to_delete = stack_names[stack_index]

    loaded_stacks.pop(stack_to_delete, None)
    updated_stack_content = json.dumps(loaded_stacks)

    try:
      with open(stack_file, "w") as file:
        file.write(updated_stack_content)
    except Exception as e:
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(e)}")
      return

    window.settings().erase(_loaded_stack_name_settings_key)
