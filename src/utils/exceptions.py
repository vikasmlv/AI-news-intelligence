"""Custom application exceptions."""


class APIError(Exception):
    """Base API error."""
    pass


class SourceError(APIError):
    """Source-related error."""
    pass


class FetchError(SourceError):
    """Error fetching from source."""
    pass


class ProcessingError(APIError):
    """Processing error."""
    pass


class ValidationError(APIError):
    """Validation error."""
    pass


class DatabaseError(APIError):
    """Database error."""
    pass


class RateLimitError(SourceError):
    """Rate limit exceeded error."""
    pass
