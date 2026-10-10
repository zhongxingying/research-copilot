# app/core/exceptions.py
class AppError(Exception):
    """所有业务异常的基类。"""

    code: str = "APP_ERROR"
    http_status: int = 500

    def __init__(self, message: str = "内部错误"):
        self.message = message
        super().__init__(message)


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    http_status = 422


class NotFoundError(AppError):
    code = "NOT_FOUND"
    http_status = 404


class LLMError(AppError):
    code = "LLM_ERROR"
    http_status = 502


class RateLimitError(AppError):
    code = "RATE_LIMIT"
    http_status = 429
