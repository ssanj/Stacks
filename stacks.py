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

_stack_file_name = "project.sublime-stack"

class StacksSaveCommand(sublime_plugin.WindowCommand):

  def run(self):
    window = self.window

    if window:
      if 'folder' in window.extract_variables():
        project_dir: str = window.extract_variables()['folder']

        views: List[ViewFileName] = [ViewFileName(v, FileName(v.file_name())) for v in window.views() if v.file_name() and not v.is_scratch() and not v.is_dirty()]
        views_to_save: List[str] = list(map(lambda v: v.file_name, views))

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
            loaded_stacks: Dict[str, Any] = json.loads(file.read())

            stack_name = _get_stack_name(window)
            has_stack_name_in_file = stack_name in loaded_stacks
            if stack_name:
              if has_stack_name_in_file:
                loaded_views: List[str] = loaded_stacks[stack_name]

                _close_open_views(window)
                for v in loaded_views:
                  window.open_file(v)
              else:
                sublime.message_dialog(f"Could not find stack named: {stack_name}")
        else:
          sublime.message_dialog(f"Could not find saved file: {saved_file}.\nPlease try saving a stack first.")
      else:
        sublime.message_dialog("Could not find project directory")

    else:
      sublime.message_dialog("No active window found")
