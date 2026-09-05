"""Service layer exception hierarchy."""


class ServiceError(Exception):
    """Base exception for all service-layer errors."""

    pass


class EntityNotFoundError(ServiceError):
    """Raised when a requested entity or parent dependency is not found."""

    pass


class ValidationError(ServiceError):
    """Raised when business validation rules are violated."""

    pass
