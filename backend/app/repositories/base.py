"""Base repository class providing shared database session handling."""

from sqlalchemy.orm import Session


class BaseRepository:
    """Base class for all repository implementations.

    Repositories accept an existing SQLAlchemy Session owned by the caller/service.
    Repositories MUST NOT commit transactions or manage session lifecycles.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the repository with a database session.

        Args:
            db: An active SQLAlchemy Session instance.
        """
        self.db = db
