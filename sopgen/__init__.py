"""
SOP-gen: AI-Powered SOP Document Generator
A modular system for generating and managing Standard Operating Procedures
"""

__version__ = "1.0.0"
__author__ = "Ganesh Gowri"

from .models import Document, Section, DocumentVersion
from .templates import TemplateManager
from .generator import AIContentGenerator
from .export import DocumentExporter

__all__ = [
    'Document',
    'Section',
    'DocumentVersion',
    'TemplateManager',
    'AIContentGenerator',
    'DocumentExporter'
]
