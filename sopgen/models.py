"""
Data Models for SOP-gen
Defines Document, Section, and Version classes
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import os


@dataclass
class Section:
    """Represents a section of an SOP document."""
    title: str                   # e.g. "Purpose", "Scope", "Responsibilities"
    content: str = ""            # The text content of the section
    content_type: str = "text"   # Type: "text", "image", "table", "flowchart", "latex"
    ai_generated: bool = False   # Flag if content was AI-generated
    locked: bool = False         # If true, section is locked from editing
    order: int = 0              # Section order in document
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def to_dict(self) -> dict:
        """Convert section to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Section':
        """Create section from dictionary"""
        return cls(**data)


@dataclass
class DocumentVersion:
    """Keeps track of a version of the document for audit trail."""
    version_id: int
    timestamp: datetime
    user: str            # username or user ID who made the changes
    role: str            # role: "doer", "reviewer", "approver", "admin"
    changes: str         # description of changes or which section edited
    content_snapshot: List[Section]  # deep copy of document sections

    def to_dict(self) -> dict:
        """Convert version to dictionary"""
        return {
            'version_id': self.version_id,
            'timestamp': self.timestamp.isoformat(),
            'user': self.user,
            'role': self.role,
            'changes': self.changes,
            'content_snapshot': [sec.to_dict() for sec in self.content_snapshot]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentVersion':
        """Create version from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['content_snapshot'] = [Section.from_dict(sec) for sec in data['content_snapshot']]
        return cls(**data)


@dataclass
class Document:
    """Encapsulates an SOP document with multiple sections and version history."""
    title: str
    doc_number: str = ""
    sections: List[Section] = field(default_factory=list)
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    versions: List[DocumentVersion] = field(default_factory=list)
    approved: bool = False      # Document finalized/approved
    approver: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)  # Company, division, etc.
    template_name: str = ""

    def add_section(self, title: str, content: str = "", content_type: str = "text", order: int = None) -> None:
        """Add a new section to the document."""
        if order is None:
            order = len(self.sections)
        self.sections.append(Section(title=title, content=content, content_type=content_type, order=order))
        self.sections.sort(key=lambda x: x.order)

    def remove_section(self, title: str) -> None:
        """Remove a section by title."""
        self.sections = [sec for sec in self.sections if sec.title != title]
        self._reorder_sections()

    def get_section(self, title: str) -> Optional[Section]:
        """Retrieve a section by title."""
        return next((sec for sec in self.sections if sec.title == title), None)

    def update_section(self, title: str, content: str, ai_generated: bool = False) -> bool:
        """Update section content"""
        section = self.get_section(title)
        if section and not section.locked:
            section.content = content
            section.ai_generated = ai_generated
            self.last_modified = datetime.now()
            return True
        return False

    def log_version(self, user: str, role: str, changes: str) -> None:
        """Log the current state as a new version."""
        version_id = len(self.versions) + 1
        snapshot = [Section(**asdict(sec)) for sec in self.sections]
        self.versions.append(
            DocumentVersion(version_id, datetime.now(), user, role, changes, snapshot)
        )
        self.last_modified = datetime.now()

    def approve(self, user: str) -> None:
        """Mark document as approved and lock all sections."""
        self.approved = True
        self.approver = user
        for sec in self.sections:
            sec.locked = True
        self.log_version(user=user, role="approver", changes="Document approved")

    def _reorder_sections(self) -> None:
        """Reorder sections after removal"""
        for idx, sec in enumerate(self.sections):
            sec.order = idx

    def to_dict(self) -> dict:
        """Convert document to dictionary for JSON serialization"""
        return {
            'title': self.title,
            'doc_number': self.doc_number,
            'sections': [sec.to_dict() for sec in self.sections],
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'versions': [ver.to_dict() for ver in self.versions],
            'approved': self.approved,
            'approver': self.approver,
            'metadata': self.metadata,
            'template_name': self.template_name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        """Create document from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_modified'] = datetime.fromisoformat(data['last_modified'])
        data['sections'] = [Section.from_dict(sec) for sec in data['sections']]
        data['versions'] = [DocumentVersion.from_dict(ver) for ver in data['versions']]
        return cls(**data)

    def save(self, directory: str = "data/documents") -> str:
        """Save document to JSON file"""
        os.makedirs(directory, exist_ok=True)
        filename = f"{self.doc_number or 'doc'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(directory, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return filepath

    @classmethod
    def load(cls, filepath: str) -> 'Document':
        """Load document from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
