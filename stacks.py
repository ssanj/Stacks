import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os
from Stacks.components.Files import FileName, ViewFileName

def _get_stack_name(window: sublime.Window) -> Optional[str]:
  return "my stack 1"

def _close_open_views(window: sublime.Window) -> None:
  views: List[sublime.View] = window.views()

  for v in views:
    v.close()

  window.run_command('set_layout', {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})

_stack_file_name = "project.sublime-stack"

# TODO: Move to Enum
def _open_stacks(window: sublime.Window, show_error: bool = True) -> Optional[Dict[str, Any]]:
  # TODO: Cache this somewhere
  project_dir: str = window.extract_variables()['folder']

  stack_file = f"{project_dir}/{_stack_file_name}"

  if os.path.exists(stack_file):
    with open(stack_file, "r") as file:
      try:
        loaded_stacks: Dict[str, Any] = json.loads(file.read())
        return loaded_stacks
      except json.decoder.JSONDecodeError:
        if show_error:
          sublime.message_dialog(f"Could not decode {stack_file}.\nConsider deleting it and resaving it or make it a valid json file.")
        else:
          # TODO: Send this to the log?
          sublime.status_message(f"Could not decode {stack_file}.\nConsider deleting it and resaving it or make it a valid json file.")

        return None
  else:
    if show_error:
      sublime.message_dialog(f"Could not find stack file:\n{stack_file}.\nPlease try saving a stack first.")
    else:
      # TODO: Send this to the log?
      sublime.status_message(f"Could not find stack file:\n{stack_file}.\nPlease try saving a stack first.")
    return None


def _get_window_state(window: sublime.Window) -> Dict[str, Any]:
  groups: List[int] = list(range(0, window.num_groups()))

  window_state: Dict[str, Any] = {}

  for g in groups:
    views_in_group = window.views_in_group(g)
    file_names: List[str] = [v.file_name() for v in views_in_group if v.file_name() and not v.is_scratch() and not v.is_dirty()] # type: ignore
    window_state.update({ f"group{g}":  file_names})

  window_state.update({ "layout": window.layout() })
  return window_state

class StacksSaveCommand(sublime_plugin.WindowCommand):

  def run(self):
    window = self.window

    if window:
      if 'folder' in window.extract_variables():
        project_dir: str = window.extract_variables()['folder']

        window.show_input_panel(
          caption = "Stack name",
          on_done = lambda sn: self.on_stack_name(project_dir, window, sn),
          initial_text = "",
          on_change = None,
          on_cancel = None
        )
      else:
        sublime.message_dialog("Could not find project directory")
    else:
      sublime.message_dialog("No active window found")

  def on_stack_name(self, project_dir: str, window: sublime.Window, stack_name: str) -> None:
    # TODO: Merge with existing values
    # TODO: if name is already taken prompt for overwrite confirmation?

    loaded_stacks: Optional[Dict[str, Any]] = _open_stacks(window, show_error = False)
    views_to_save = _get_window_state(window)

    stacks_to_save: Dict[str, Any] = loaded_stacks if loaded_stacks else {}
    stacks_to_save.update({ stack_name : views_to_save})
    new_stack_json_content: str = json.dumps(stacks_to_save)

    try:
      with open(f"{project_dir}/{_stack_file_name}", "w") as file:
        file.write(new_stack_json_content)
    except Exception as e:
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(e)}")
      return

    # TODO: Do we need to move this option to config?
    _close_open_views(window)


class StacksOpenCommand(sublime_plugin.WindowCommand):

  def run(self):
    window = self.window

    if window:
      if 'folder' in window.extract_variables():
        project_dir: str = window.extract_variables()['folder']

        stack_file = f"{project_dir}/{_stack_file_name}"

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
              placeholder = "Which stack would you like to load?",
              on_select = lambda index: self.on_stack_load(stack_file, window, loaded_stacks, items, index)
            )

        else:
          sublime.message_dialog(f"Could not find saved file:\n{stack_file}.\nPlease try saving a stack first.")
      else:
        sublime.message_dialog("Could not find project directory")

    else:
      sublime.message_dialog("No active window found")

  def on_stack_load(self, stack_file: str, window: sublime.Window, loaded_stacks: Dict[str, Any], stack_names: List[str], stack_index: int) -> None:
    if stack_index < 0 or stack_index > len(stack_names):
      return

    stack_name = stack_names[stack_index]

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
    else:
      sublime.message_dialog(f"Could not find stack named:\n{stack_name}\nin:\n{stack_file}")

