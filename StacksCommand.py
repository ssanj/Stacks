from abc import abstractmethod
import sublime
import sublime_plugin
from Stacks.components.Common import _stack_file_name, _close_open_views, _loaded_stack_name_settings_key

class StacksCommand(sublime_plugin.WindowCommand):

  project_dir = None
  stack_file = None

  def run(self):
    window = self.window

    if window:
      if not StacksCommand.project_dir:
         if 'folder' in window.extract_variables():
            StacksCommand.project_dir: str = window.extract_variables()['folder']
            StacksCommand.stack_file = f"{StacksCommand.project_dir}/{_stack_file_name}"
            # remove any saved stack names on restart
            window.settings().erase(_loaded_stack_name_settings_key)
            print(f"setting project_dir and stack file")
         else:
            sublime.message_dialog("Could not find project directory")
      else:
        print(f"project_dir is already set!")
        pass #project_dir and stack_file have been set

      self.on_run(window, StacksCommand.stack_file)
    else:
      sublime.message_dialog("No active window found")

  @abstractmethod
  def on_run(self, window: sublime.Window, stack_file: str) -> None:
    pass
