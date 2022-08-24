import sublime
import sublime_plugin
from typing import Optional
from Stacks.components.Common import _loaded_stack_name_settings_key

class StacksShowStackNameCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    view: sublime.View = self.view
    window: sublime.View = self.view.window()

    if window and view:
      stack_name: Optional[str] = window.settings().get(_loaded_stack_name_settings_key)
      display_text: str = f"Stack Name: {stack_name}" if stack_name else "No Stack name found"
      view.show_popup(f"<h2>{display_text}</h2>", max_width=640, max_height=480)
