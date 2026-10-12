class BaseAppException(Exception):
    """Базовый класс для всех исключений приложения"""
    pass

class OTPErrorSending(BaseAppException):
    pass

class SMTPAuthenticationError(BaseAppException):
    pass

class SMTPRecipientRefused(BaseAppException):
    pass

class SMTPException(BaseAppException):
    pass