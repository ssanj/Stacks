import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Common import _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.components.FileUtils import LoadError, load_stack_file
from Stacks.components.Files import StackFileName
from Stacks.components.ResultTypes import Either, RightEither, LeftEither
from Stacks.StacksLoaderCommand import StacksLoaderCommand, SelectedStackName

class StacksOpenCommand(StacksLoaderCommand):

  def loader_message(self) -> str:
    return "Which stack would you like to load?"

  def on_stack_name_selected(self, stack_file: StackFileName, window: sublime.Window, loaded_stacks: Dict[str, Any], selected_stack_name: SelectedStackName) -> None:
    stack_name = selected_stack_name.value

    # TODO: Validate stack_name
    has_stack_name_in_file = stack_name in loaded_stacks
    if has_stack_name_in_file:
      window_state: Dict[str, Any] = loaded_stacks[stack_name]

      _close_open_views(window)
      window.set_layout(window_state['layout'])

      # TODO make this safer or use a regex
      key_groups: List[int] = [int(key.split("group")[1]) for key in window_state.keys() if key.startswith("group")]

      for group in key_groups:
        views_in_group = window_state[f"group{group}"]
        for v in views_in_group:
          # TODO: Check if the file still exists
          window.open_file(fname = v, group = group)

      window.settings().update({_loaded_stack_name_settings_key : stack_name})
      print(f"stack loaded: {stack_name}")
    else:
      sublime.message_dialog(f"Could not find stack named:\n{stack_name}\nin:\n{stack_file.value}")
