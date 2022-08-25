from abc import abstractmethod
import sublime
import sublime_plugin
from Stacks.components.Common import _stack_file_name, _loaded_stack_name_settings_key
from Stacks.components.Files import StackFileName
from typing import Optional
import logging

class StacksCommand(sublime_plugin.WindowCommand):

  project_dir: Optional[str] = None
  stack_file: Optional[StackFileName] = None
  FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'
  logging.basicConfig(format=FORMAT)

  def run(self):
    self.class_name = type(self).__name__
    self.logger: logging.Logger = logging.getLogger(f"[Stacks:{self.class_name}]")
    self.logger.setLevel(logging.INFO)
    window = self.window

    if window:
      if not StacksCommand.project_dir:
         if 'folder' in window.extract_variables():
            StacksCommand.project_dir: str = window.extract_variables()['folder']
            StacksCommand.stack_file = StackFileName(f"{StacksCommand.project_dir}/{_stack_file_name}")
            # # remove any saved stack names on restart
            # window.settings().erase(_loaded_stack_name_settings_key)
            self.logger.info(f"setting project_dir and stack file")
         else:
            sublime.message_dialog("Could not find project directory")
      else:
        self.logger.info(f"project_dir is already set!")
        pass #project_dir and stack_file have been set

      self.on_run(window, StacksCommand.stack_file, self.logger)
    else:
      sublime.message_dialog("No active window found")

  @abstractmethod
  def on_run(self, window: sublime.Window, stack_file: StackFileName, logger: logging.Logger) -> None:
    pass
