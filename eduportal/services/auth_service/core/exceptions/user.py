from .abc import AbstractException, ConflictException, NotFoundException


class UserException(AbstractException):
    """Base user exception."""


class UserNotFoundException(UserException, NotFoundException):
    """User not found."""

    detail = "User not found"


class UserDeletedException(UserException, ConflictException):
    """User deleted."""

    detail = "User deleted"
