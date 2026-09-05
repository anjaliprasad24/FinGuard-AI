"""PII Scrubber Service for masking sensitive personal information."""

import re


class PIIScrubber:
    """Regex based PII masker for merchant strings, receipts, and user prompts."""

    CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
    PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b")
    PHONE_PATTERN = re.compile(r"\b(?:\+91|0)?[6-9]\d{9}\b")
    EMAIL_PATTERN = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")

    @classmethod
    def scrub(cls, text: str) -> str:
        if not text:
            return ""

        scrubbed = text

        # Mask Credit/Debit Cards
        def mask_card(match: re.Match) -> str:
            raw_digits = re.sub(r"\D", "", match.group(0))
            last4 = raw_digits[-4:] if len(raw_digits) >= 4 else "XXXX"
            return f"****-****-****-{last4}"

        scrubbed = cls.CARD_PATTERN.sub(mask_card, scrubbed)

        # Mask PAN
        scrubbed = cls.PAN_PATTERN.sub("[PAN_REDACTED]", scrubbed)

        # Mask Phone
        scrubbed = cls.PHONE_PATTERN.sub("[PHONE_REDACTED]", scrubbed)

        # Mask Email
        scrubbed = cls.EMAIL_PATTERN.sub("[EMAIL_REDACTED]", scrubbed)

        return scrubbed
