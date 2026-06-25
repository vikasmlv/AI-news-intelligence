"""Data validation utilities."""

from typing import List, Optional
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """Validate URL format.

    Args:
        url: URL string to validate

    Returns:
        True if URL is valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Validate email format.

    Args:
        email: Email string to validate

    Returns:
        True if email is valid
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_text(text: str) -> str:
    """Clean and normalize text.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text (simple implementation).

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords

    Returns:
        List of keywords
    """
    # Split into words and filter by length
    words = text.lower().split()
    keywords = [w.strip(',.!?;:') for w in words if len(w) > 3]
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for k in keywords:
        if k not in seen:
            result.append(k)
            seen.add(k)
            if len(result) >= max_keywords:
                break
    return result
