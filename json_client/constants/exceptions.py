"""
    Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
    Author Alexandr Zagorskiy
"""

from enum import Enum


class CommonError(Exception):
    def __init__(self, error: Exception, msg: str):
        super().__init__(msg)
        self.msg = f"{error.value}: {msg}"


class InvalidValueError(CommonError):
    def __init__(self, msg: str):
        super().__init__(CommonErrorMessages.INVALID_VALUE, msg)


class InvalidStateError(CommonError):
    def __init__(self, msg: str):
        super().__init__(CommonErrorMessages.INVALID_STATE, msg)


class LinkContentOversizeError(CommonError):
    def __init__(self, msg: str):
        super().__init__(CommonErrorMessages.LINK_OVERSIZE, msg)


class CommonErrorMessages(Enum):
    INVALID_STATE = "Invalid state"
    INVALID_VALUE = "Invalid value"
    MERGE_ERROR = "You can't merge two different syntax type"
    LINK_OVERSIZE = "Link content exceeds permissible value"
