from Stacks.components.ResultTypes import Either, LeftEither, RightEither
from typing import Dict, Any
from enum import Enum, auto, unique
import json
import os

@unique
class LoadError(Enum):
  STACK_FILE_NOT_FOUND = auto()
  COULD_NOT_DECODE_STACK_FILE = auto()

def load_stack_file(stack_file: str) -> Either[LoadError, Dict[str, Any]]:
  if os.path.exists(stack_file):
    with open(stack_file, "r") as file:
      try:
        loaded_stacks: Dict[str, Any] = json.loads(file.read())
        return RightEither(loaded_stacks)
      except json.decoder.JSONDecodeError:
        return LeftEither(LoadError.COULD_NOT_DECODE_STACK_FILE)
  else:
    return LeftEither(LoadError.STACK_FILE_NOT_FOUND)

