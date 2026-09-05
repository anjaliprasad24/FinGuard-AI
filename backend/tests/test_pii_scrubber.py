"""Unit tests for PII Scrubber."""

from app.services.pii_scrubber import PIIScrubber


def test_pii_scrubber_card_masking():
    raw = "Purchase at Apple Store with card 4532-1111-2222-9988"
    scrubbed = PIIScrubber.scrub(raw)
    assert "****-****-****-9988" in scrubbed
    assert "4532-1111-2222-9988" not in scrubbed


def test_pii_scrubber_pan_and_phone():
    raw = "PAN ABCDE1234F Phone 9876543210"
    scrubbed = PIIScrubber.scrub(raw)
    assert "[PAN_REDACTED]" in scrubbed
    assert "[PHONE_REDACTED]" in scrubbed


def test_pii_scrubber_email():
    raw = "Contact user@example.com for receipt"
    scrubbed = PIIScrubber.scrub(raw)
    assert "[EMAIL_REDACTED]" in scrubbed
