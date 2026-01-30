"""Custom exceptions for the finance app."""


class NoKeyFinanceError(Exception):
    """Base exception for this application."""

    pass


class DataSourceError(NoKeyFinanceError):
    """Raised when a data source fails (fetch, parse, etc.)."""

    pass


class ValidationError(NoKeyFinanceError):
    """Raised when input validation fails (ticker, dates, etc.)."""

    pass


class IndicatorError(NoKeyFinanceError):
    """Raised when indicator computation fails."""

    pass
