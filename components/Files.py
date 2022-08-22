from typing import NamedTuple

import sublime

class FileName(NamedTuple):
  value: str

class ViewFileName(NamedTuple):
  view: sublime.View
  file_name: FileName
