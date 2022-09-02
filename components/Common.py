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


def _get_window_state(window: sublime.Window) -> Dict[str, Any]:
  groups: List[int] = list(range(0, window.num_groups()))

  window_state: Dict[str, Any] = {}

  for g in groups:
    views_in_group = window.views_in_group(g)
    file_names: List[str] = [v.file_name() for v in views_in_group if v.file_name() and not v.is_scratch() and not v.is_dirty()] # type: ignore
    window_state.update({ f"group{g}":  file_names})

  window_state.update({ "layout": window.layout() })
  return window_state
