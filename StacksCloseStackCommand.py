import sublime
import sublime_plugin
from typing import Optional
from Stacks.components.Common import _loaded_stack_name_settings_key, _close_open_views

class StacksCloseStackCommand(sublime_plugin.WindowCommand):

  def run(self):
    window: sublime.Window = self.window

    if window:
      _close_open_views(window)
      window.settings().erase(_loaded_stack_name_settings_key)
