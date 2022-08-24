from typing import NamedTuple, TypeVar, Generic

from abc import abstractmethod

L = TypeVar('L')
R = TypeVar('R')

class Either(Generic[L, R]):

  @abstractmethod
  def is_error(self) -> bool:
    pass

  @abstractmethod
  def has_value(self) -> bool:
    pass

  @abstractmethod
  def value(self) -> R:
    pass

  @abstractmethod
  def error(self) -> L:
    pass


class RightEither(Either[L, R], Generic[L, R]):

  def __init__(self, right: R) -> None:
    self.right = right

  def is_error(self) -> bool:
   return False

  def has_value(self) -> bool:
    return True

  def value(self)-> R:
    return self.right

  def error(self)-> L:
    raise TypeError("Calling error on Right")


class LeftEither(Either[L, R], Generic[L, R]):

  def __init__(self, left: L) -> None:
    self.left = left

  def is_error(self) -> bool:
   return True

  def has_value(self) -> bool:
    return False

  def value(self)-> R:
    raise TypeError("Calling value on Left")

  def error(self)-> L:
    return self.left
