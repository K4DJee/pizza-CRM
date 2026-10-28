class BaseAppException(Exception):
    """Базовый класс для всех исключений приложения"""
    pass

class InternalServerError(BaseAppException):
    pass