class BaseAppException(Exception):
    """Базовый класс для всех исключений приложения"""
    pass

class DishNotFound(BaseAppException):
    pass

class PermissionDenied(BaseAppException):
    pass

class InvalidAuthHeader(BaseAppException):
    pass

class PermissionDenied(BaseAppException):
    pass

class ErrorCreatingDish(BaseAppException):
    pass

class IngredientNotExists(BaseAppException):
    pass

class RequestError(BaseAppException):
    pass