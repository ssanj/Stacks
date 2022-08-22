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

        # views: List[ViewFileName] = [ViewFileName(v, FileName(v.file_name())) for v in window.views() if v.file_name() and not v.is_scratch() and not v.is_dirty()]
        # views_to_save: List[str] = list(map(lambda v: v.file_name.value, views))
        views_to_save = _get_window_state(window)

        # TODO: Merge with existing values
        json_content: str = json.dumps({ _get_stack_name(window) : views_to_save})

        with open(f"{project_dir}/{_stack_file_name}", "w") as file:
           file.write(json_content)

        # TODO: Do we need to move this option to config?
        _close_open_views(window)
      else:
        sublime.message_dialog("Could not find project directory")
    else:
      sublime.message_dialog("No active window found")

class StacksOpenCommand(sublime_plugin.WindowCommand):

  def run(self):
    window = self.window

    if window:
      if 'folder' in window.extract_variables():
        project_dir: str = window.extract_variables()['folder']

        saved_file = f"{project_dir}/{_stack_file_name}"

        if os.path.exists(saved_file):
          with open(saved_file, "r") as file:
            try:
              loaded_stacks: Dict[str, Any] = json.loads(file.read())
            except json.decoder.JSONDecodeError:
              sublime.message_dialog(f"Could not decode {saved_file}.\nConsider deleting it and resaving it or make it a valid json file.")
              return

            stack_name = _get_stack_name(window)
            has_stack_name_in_file = stack_name in loaded_stacks
            if stack_name:
              if has_stack_name_in_file:
                loaded_views: List[str] = loaded_stacks[stack_name]

                _close_open_views(window)
                for v in loaded_views:
                  window.open_file(v)
              else:
                sublime.message_dialog(f"Could not find stack named:\n{stack_name}\nin:\n{saved_file}")

        else:
          sublime.message_dialog(f"Could not find saved file:\n{saved_file}.\nPlease try saving a stack first.")
      else:
        sublime.message_dialog("Could not find project directory")

    else:
      sublime.message_dialog("No active window found")
