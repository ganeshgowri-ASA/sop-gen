"""
Template Library Management
Handles predefined templates and custom template imports
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path
from .models import Document, Section


class TemplateManager:
    """Manages SOP templates and template library"""

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self._ensure_templates_dir()

    def _ensure_templates_dir(self):
        """Ensure templates directory exists"""
        os.makedirs(self.templates_dir, exist_ok=True)

    def list_templates(self) -> List[str]:
        """Return list of available template names"""
        templates = []
        if os.path.exists(self.templates_dir):
            for file in os.listdir(self.templates_dir):
                if file.endswith('.json'):
                    templates.append(file.replace('.json', ''))
        return sorted(templates)

    def load_template(self, template_name: str) -> Document:
        """Load a predefined template by name and return a Document"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.json")

        if not os.path.exists(template_path):
            raise ValueError(f"Template '{template_name}' not found at {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)

        # Create document from template
        doc = Document(
            title=template_data.get('title', f'{template_name} SOP'),
            doc_number=template_data.get('doc_number', ''),
            created_by='template_system',
            template_name=template_name,
            metadata=template_data.get('metadata', {})
        )

        # Add sections from template
        for idx, section_data in enumerate(template_data.get('sections', [])):
            doc.add_section(
                title=section_data['title'],
                content=section_data.get('content', ''),
                content_type=section_data.get('content_type', 'text'),
                order=idx
            )

        return doc

    def save_template(self, template_name: str, template_data: dict) -> str:
        """Save a template to the library"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.json")

        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=2, ensure_ascii=False)

        return template_path

    def import_template_from_dict(self, template_data: dict) -> Document:
        """Import a custom template from dictionary"""
        doc = Document(
            title=template_data.get('title', 'Untitled SOP'),
            doc_number=template_data.get('doc_number', ''),
            created_by='user',
            metadata=template_data.get('metadata', {})
        )

        for idx, section_data in enumerate(template_data.get('sections', [])):
            doc.add_section(
                title=section_data['title'],
                content=section_data.get('content', ''),
                content_type=section_data.get('content_type', 'text'),
                order=idx
            )

        return doc

    def get_template_info(self, template_name: str) -> Optional[dict]:
        """Get template metadata and section list"""
        template_path = os.path.join(self.templates_dir, f"{template_name}.json")

        if not os.path.exists(template_path):
            return None

        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)

        return {
            'name': template_name,
            'title': template_data.get('title', ''),
            'description': template_data.get('description', ''),
            'standard': template_data.get('standard', ''),
            'section_count': len(template_data.get('sections', [])),
            'sections': [s['title'] for s in template_data.get('sections', [])]
        }


class StandardsManager:
    """Manages standards database and references"""

    def __init__(self):
        self.standards_db = self._initialize_standards()

    def _initialize_standards(self) -> Dict[str, dict]:
        """Initialize standards database"""
        return {
            # IEC Standards (PV Testing)
            "IEC 61215": {
                "full_name": "IEC 61215: Terrestrial photovoltaic (PV) modules - Design qualification and type approval",
                "category": "Solar PV",
                "organization": "IEC",
                "description": "Design qualification and type approval for crystalline silicon PV modules"
            },
            "IEC 61730": {
                "full_name": "IEC 61730: Photovoltaic (PV) module safety qualification",
                "category": "Solar PV",
                "organization": "IEC",
                "description": "Safety qualification requirements for PV modules"
            },
            "IEC 61853": {
                "full_name": "IEC 61853: Photovoltaic (PV) module performance testing and energy rating",
                "category": "Solar PV",
                "organization": "IEC",
                "description": "PV module performance testing procedures and energy rating methodologies"
            },
            "IEC 62804": {
                "full_name": "IEC 62804: Test methods for the detection of potential-induced degradation of crystalline silicon PV modules",
                "category": "Solar PV",
                "organization": "IEC",
                "description": "Methods for detecting potential-induced degradation (PID) in PV modules"
            },

            # ISO Standards (Quality & Management)
            "ISO 9001": {
                "full_name": "ISO 9001: Quality management systems - Requirements",
                "category": "Quality Management",
                "organization": "ISO",
                "description": "Requirements for quality management systems"
            },
            "ISO 14001": {
                "full_name": "ISO 14001: Environmental management systems - Requirements with guidance for use",
                "category": "Environmental Management",
                "organization": "ISO",
                "description": "Environmental management system requirements"
            },
            "ISO 45001": {
                "full_name": "ISO 45001: Occupational health and safety management systems - Requirements with guidance for use",
                "category": "Health & Safety",
                "organization": "ISO",
                "description": "Occupational health and safety management requirements"
            },
            "ISO 27001": {
                "full_name": "ISO 27001: Information security management systems - Requirements",
                "category": "Information Security",
                "organization": "ISO",
                "description": "Information security management system requirements"
            },
            "ISO 17025": {
                "full_name": "ISO/IEC 17025: General requirements for the competence of testing and calibration laboratories",
                "category": "Laboratory Testing",
                "organization": "ISO",
                "description": "Requirements for competence of testing and calibration laboratories"
            },

            # ASTM Standards
            "ASTM E1036": {
                "full_name": "ASTM E1036: Standard Test Methods for Electrical Performance of Nonconcentrator Terrestrial Photovoltaic Modules and Arrays Using Reference Cells",
                "category": "Solar PV",
                "organization": "ASTM",
                "description": "Test methods for PV module electrical performance"
            },
            "ASTM D7866": {
                "full_name": "ASTM D7866: Standard Test Method for Determining the Biobased Content of Solid, Liquid, and Gaseous Samples Using Radiocarbon Analysis",
                "category": "Materials Testing",
                "organization": "ASTM",
                "description": "Radiocarbon analysis for biobased content"
            }
        }

    def get_all_standards(self) -> Dict[str, dict]:
        """Return all standards"""
        return self.standards_db

    def get_standard(self, standard_id: str) -> Optional[dict]:
        """Get specific standard information"""
        return self.standards_db.get(standard_id)

    def search_standards(self, query: str) -> Dict[str, dict]:
        """Search standards by keyword"""
        query = query.lower()
        results = {}
        for std_id, std_data in self.standards_db.items():
            if (query in std_id.lower() or
                query in std_data['full_name'].lower() or
                query in std_data['category'].lower()):
                results[std_id] = std_data
        return results

    def get_citation(self, standard_id: str) -> str:
        """Get formatted citation for a standard"""
        std = self.get_standard(standard_id)
        if std:
            return f"{standard_id}: {std['full_name']}"
        return standard_id
