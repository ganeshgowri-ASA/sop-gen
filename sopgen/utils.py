"""
Utility functions for SOP-gen
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime


def ensure_directory(directory: str) -> None:
    """Ensure directory exists, create if not"""
    os.makedirs(directory, exist_ok=True)


def get_saved_documents(directory: str = "data/documents") -> List[str]:
    """Get list of saved document files"""
    if not os.path.exists(directory):
        return []

    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    return sorted(files, reverse=True)  # Most recent first


def format_timestamp(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system use"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def get_file_size_mb(file_bytes: bytes) -> float:
    """Get file size in MB"""
    return len(file_bytes) / (1024 * 1024)


def validate_document(doc_data: dict) -> tuple[bool, str]:
    """
    Validate document data

    Returns:
        (is_valid, error_message)
    """
    required_fields = ['title', 'sections']

    for field in required_fields:
        if field not in doc_data:
            return False, f"Missing required field: {field}"

    if not doc_data['title'].strip():
        return False, "Document title cannot be empty"

    if not doc_data['sections']:
        return False, "Document must have at least one section"

    return True, ""


def generate_doc_number(prefix: str = "SOP", category: str = "") -> str:
    """Generate a document number"""
    timestamp = datetime.now().strftime('%Y%m%d')

    if category:
        return f"{prefix}-{category.upper()}-{timestamp}"
    else:
        return f"{prefix}-{timestamp}"


class Colors:
    """Color constants for UI"""
    PRIMARY = "#FF6B35"
    SECONDARY = "#004E89"
    SUCCESS = "#28a745"
    WARNING = "#ffc107"
    DANGER = "#dc3545"
    INFO = "#17a2b8"
    LIGHT = "#f8f9fa"
    DARK = "#343a40"
