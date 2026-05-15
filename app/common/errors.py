class AppException(Exception):
    """Base application exception for expected domain and application errors."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: object | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details: object | None = None) -> None:
        super().__init__(status_code=400, code="BAD_REQUEST", message=message, details=details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: object | None = None) -> None:
        super().__init__(status_code=404, code="NOT_FOUND", message=message, details=details)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict", details: object | None = None) -> None:
        super().__init__(status_code=409, code="CONFLICT", message=message, details=details)
