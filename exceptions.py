"""Custom exceptions for the Notion SDK."""


class NotionError(Exception):
    """Base exception for all Notion SDK errors."""

    pass


class NotionAPIError(NotionError):
    """Raised when a Notion API request fails."""

    def __init__(self, message: str, status_code: int | None = None, error_code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code

    def __str__(self) -> str:
        return f"NotionAPIError: {self.args[0]} (Status: {self.status_code}, Code: {self.error_code})"


class NotionRateLimitError(NotionAPIError):
    """Raised when the Notion API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int | None = None):
        super().__init__(message, status_code=429, error_code="rate_limited")
        self.retry_after = retry_after


class NotionBadRequestError(NotionAPIError):
    """Raised for 400 Bad Request errors."""

    pass


class NotionAuthenticationError(NotionAPIError):
    """Raised for 401 Unauthorized errors."""

    pass


class NotionPermissionError(NotionAPIError):
    """Raised for 403 Forbidden errors."""

    pass


class NotionNotFoundError(NotionAPIError):
    """Raised for 404 Not Found errors."""

    pass


class NotionConflictError(NotionAPIError):
    """Raised for 409 Conflict errors."""

    pass


class NotionInternalServerError(NotionAPIError):
    """Raised for 5xx server errors."""

    pass


class NotionServiceUnavailableError(NotionAPIError):
    """Raised for 503 Service Unavailable errors."""

    pass

