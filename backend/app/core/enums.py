"""Shared domain enums for statuses and entity types."""

from enum import Enum


class SessionStatus(str, Enum):
    """Lifecycle status of an interaction/capture session."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABANDONED = "ABANDONED"


class ProcessingJobStatus(str, Enum):
    """Lifecycle status of an asynchronous processing job."""

    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class MemoryType(str, Enum):
    """Semantic type classification for durable memories."""

    SUMMARY = "SUMMARY"
    EPISODIC = "EPISODIC"
    FACT = "FACT"
    NOTE = "NOTE"


class MemorySourceType(str, Enum):
    """Type of context evidence supporting a memory."""

    TRANSCRIPT = "TRANSCRIPT"
    VISUAL_CONTEXT = "VISUAL_CONTEXT"
    INTERACTION = "INTERACTION"
    CAPTURE_SEGMENT = "CAPTURE_SEGMENT"


class MemoryFeedbackType(str, Enum):
    """User feedback classification for a generated memory."""

    HELPFUL = "HELPFUL"
    NOT_HELPFUL = "NOT_HELPFUL"
    DISMISS = "DISMISS"
