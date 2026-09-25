class BaseAppException(Exception):
    """Базовый класс для всех исключений приложения"""
    pass


class UserNotFoundError(BaseAppException):
    pass

class InvalidTokenPayload(BaseAppException):
    pass

class InvalidTokenError(BaseAppException):
    pass

class OTPErrorSending(BaseAppException):
    pass

class OTPExists(BaseAppException):
    pass

class OTPNotFound(BaseAppException):
    pass

class OTPNotMatch(BaseAppException):
    pass

class ReetTokenExists(BaseAppException):
    pass

class ResetTokenNotFound(BaseAppException):
    pass

class ResetTokenNotMatch(BaseAppException):
    pass

class DishNotFound(BaseAppException):
    pass

class PermissionDenied(BaseAppException):
    pass

class InvalidAuthHeader(BaseAppException):
    pass

class PermissionDenied(BaseAppException):
    pass