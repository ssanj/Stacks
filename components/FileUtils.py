from Stacks.components.ResultTypes import Either, LeftEither, RightEither
from typing import Dict, Any, NamedTuple
from enum import Enum, auto, unique
import json
import os

from Stacks.components.Files import StackFileName

@unique
class LoadError(Enum):
  STACK_FILE_NOT_FOUND = auto()
  COULD_NOT_DECODE_STACK_FILE = auto()

class SaveError(NamedTuple):
  value: Exception

def load_stack_file(stack_file: StackFileName) -> Either[LoadError, Dict[str, Any]]:
  if os.path.exists(stack_file.value):
    with open(stack_file.value, "r") as file:
      try:
        loaded_stacks: Dict[str, Any] = json.loads(file.read())
        return RightEither(loaded_stacks)
      except json.decoder.JSONDecodeError:
        return LeftEither(LoadError.COULD_NOT_DECODE_STACK_FILE)
  else:
    return LeftEither(LoadError.STACK_FILE_NOT_FOUND)


def save_stack_file(stack_file: StackFileName, json_content: str) -> Either[SaveError, None]:
  try:
    with open(stack_file.value, "w") as file:
      file.write(json_content)
      return RightEither(None)
  except Exception as e:
    return LeftEither(SaveError(e))

