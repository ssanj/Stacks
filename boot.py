import sublime
from Stacks.components.Common import _loaded_stack_name_settings_key

def plugin_loaded() -> None:
  print("stack is resetting saved stacks")
  for w in sublime.windows():
    w.settings().erase(_loaded_stack_name_settings_key)


def plugin_unloaded() -> None:
  print("---------------> Stacks unloaded")
