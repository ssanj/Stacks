import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksCommand import StacksCommand

class StacksRenameCommand(StacksCommand):

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
          placeholder = "Which stack would you like to rename?",
          on_select = lambda index: self.on_stack_rename_selection(stack_file, window, loaded_stacks, items, index)
        )
    else:
      sublime.message_dialog(f"Could not find saved file:\n{stack_file}.\nPlease try saving a stack first.")

  def on_stack_rename_selection(self, stack_file: str, window: sublime.Window, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_index: int) -> None:
    if stack_index < 0 or stack_index > len(stack_names):
      return

    stack_to_rename = stack_names[stack_index]

    window.show_input_panel(
      caption = "Stack name",
      on_done = lambda new_stack_name: self.on_stack_rename(stack_file, stack_to_rename, loaded_stacks, window, new_stack_name),
      initial_text = "",
      on_change = None,
      on_cancel = None
    )

  def on_stack_rename(self, stack_file: str, old_stack_name: str, loaded_stacks: Dict[str, Any], window: sublime.Window, new_stack_name: str) -> None:

    stack_content = loaded_stacks.pop(old_stack_name, None)

    # we found the existing stack for the old name
    if stack_content:
      loaded_stacks.update({new_stack_name : stack_content})
    else:
      # Add an empty stack if things have gone wrong
      loaded_stacks.update({new_stack_name : {}})

    updated_stack_content = json.dumps(loaded_stacks)

    try:
      with open(stack_file, "w") as file:
        file.write(updated_stack_content)
    except Exception as e:
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(e)}")
      return

    # get the currently loaded stack name
    current_stack_name = window.settings().get(_loaded_stack_name_settings_key)

    # if it matches the old stack name, then rename it in the settings
    if current_stack_name and current_stack_name == old_stack_name:
      window.settings().update({ _loaded_stack_name_settings_key: new_stack_name})

