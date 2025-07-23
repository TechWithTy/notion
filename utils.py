"""Utility functions for the Notion SDK."""

import re

def clean_id(id_str: str) -> str:
    """Removes dashes from a Notion ID to get the 32-character format.

    Args:
        id_str: The Notion ID, which may or may not contain dashes.

    Returns:
        The cleaned 32-character ID.
    """
    return id_str.replace("-", "")


def is_valid_notion_id(id_str: str) -> bool:
    """Checks if a string is a valid 32-character hexadecimal Notion ID.

    Args:
        id_str: The string to validate.

    Returns:
        True if the string is a valid Notion ID, False otherwise.
    """
    cleaned = clean_id(id_str)
    return len(cleaned) == 32 and re.fullmatch(r"[0-9a-f]+", cleaned) is not None
