import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict
import json
import os

def _close_open_views(window: sublime.Window) -> None:
  views: List[sublime.View] = window.views()

  for v in views:
    v.close()

  window.run_command('set_layout', {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})

_stack_file_name = "project.sublime-stack"

_loaded_stack_name_settings_key = "stacks.name"

# TODO: Move to Enum
def _open_stacks(window: sublime.Window, show_error: bool = True) -> Optional[Dict[str, Any]]:
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
