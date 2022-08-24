import sublime
import sublime_plugin
from typing import Optional, Any, Dict
import json
from Stacks.components.Common import _open_stacks, _get_window_state, _stack_file_name, _close_open_views, _loaded_stack_name_settings_key
from Stacks.StacksCommand import StacksCommand

class StacksSaveCommand(StacksCommand):

  def on_run(self, window: sublime.Window, stack_file: str):
    loaded_stack_name = window.settings().get(_loaded_stack_name_settings_key)

    if loaded_stack_name:
      update_stack = sublime.yes_no_cancel_dialog(f"Update stack: {loaded_stack_name}")
      if update_stack == sublime.DIALOG_YES:
        return self.on_stack_name(stack_file, window, loaded_stack_name)
      elif update_stack == sublime.DIALOG_CANCEL:
        return
      else:
        pass #ask for new name
    else:
      pass

    window.show_input_panel(
      caption = "Stack name",
      on_done = lambda sn: self.on_stack_name(stack_file, window, sn),
      initial_text = "",
      on_change = None,
      on_cancel = None
    )

  def on_stack_name(self, stack_file: str, window: sublime.Window, stack_name: str) -> None:
    # TODO: Merge with existing values
    # TODO: if name is already taken prompt for overwrite confirmation?

    loaded_stacks: Optional[Dict[str, Any]] = _open_stacks(window, show_error = False)
    views_to_save = _get_window_state(window)

    stacks_to_save: Dict[str, Any] = loaded_stacks if loaded_stacks else {}
    stacks_to_save.update({ stack_name : views_to_save})
    new_stack_json_content: str = json.dumps(stacks_to_save)

    try:
      with open(stack_file, "w") as file:
        file.write(new_stack_json_content)
    except Exception as e:
      sublime.message_dialog(f"Could not save stack.\nError:\n{str(e)}")
      return

    close_all_windows = sublime.yes_no_cancel_dialog("Close all windows?")
    if close_all_windows == sublime.DIALOG_YES:
      # TODO: Do we need to move this option to config?
      _close_open_views(window)
      # Remove stack name of save and close
      window.settings().erase(_loaded_stack_name_settings_key)
    else:
      # Set stack name on save and leave open
      window.settings().update({_loaded_stack_name_settings_key : stack_name})
