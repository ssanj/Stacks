from abc import abstractmethod
import sublime
import sublime_plugin
from Stacks.components.Common import _stack_file_name, _loaded_stack_name_settings_key
from Stacks.components.Files import StackFileName
from typing import Optional
import logging

class StacksCommand(sublime_plugin.WindowCommand):

  stack_file: Optional[StackFileName] = None
  FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'
  logging.basicConfig(format=FORMAT)

  def run(self):
    self.class_name = type(self).__name__
    self.logger: logging.Logger = logging.getLogger(f"[Stacks:{self.class_name}]")
    self.logger.setLevel(logging.INFO)
    window = self.window

    if window:
      if 'folder' in window.extract_variables():
        self.project_dir: str = window.extract_variables()['folder']
        self.stack_file = StackFileName(f"{self.project_dir}/{_stack_file_name}")
        # # remove any saved stack names on restart
        # window.settings().erase(_loaded_stack_name_settings_key)
        self.logger.info(f"setting project_dir: {self.project_dir} and stack file {self.stack_file.value}")
        self.on_run(window, self.logger, self.stack_file)
      else:
        sublime.message_dialog("Could not find project directory")
    else:
      sublime.message_dialog("No active window found")

  @abstractmethod
  def on_run(self, window: sublime.Window, logger: logging.Logger, stack_file: StackFileName) -> None:
    pass
