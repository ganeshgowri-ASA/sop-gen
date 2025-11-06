# SOP-gen: AI-Powered SOP Document Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SOP-gen** is an AI-driven application for generating and managing Standard Operating Procedures (SOPs), lab manuals, quality procedures, and similar documents. It combines a comprehensive template library of industry standards with intelligent content generation to help engineers, scientists, QA professionals, and lab technicians create user-specific SOPs quickly and collaboratively.

![SOP-gen Banner](https://via.placeholder.com/800x200?text=SOP-gen+AI-Powered+Document+Generator)

## 🌟 Key Features

### 📚 **Template & Document Library**
- **10+ Pre-loaded Templates** for industry standards:
  - **IEC Standards**: 61215, 61730, 61853, 62804 (Solar PV)
  - **ISO Standards**: 9001, 14001, 17025, 27001, 45001
  - **Generic SOP** template
- Upload and manage custom templates
- Template metadata and section previews

### 🤖 **AI-Assisted Content Generation**
- **Multi-Model Support**: OpenAI GPT-4, Anthropic Claude
- **Intelligent Routing**: Automatically selects the best AI model for each section type
- **Demo Mode**: Works without API keys using mock responses for testing
- **Customizable Prompts**: Tailor AI generation to your specific needs
- Generate professional content for:
  - Purpose, Scope, Procedures
  - Risk Assessments, Equipment Lists
  - Data Analysis, Pass/Fail Criteria
  - And more...

### ✍️ **Smart Document Builder**
- **Section-by-Section Editing**: Intuitive interface for precise control
- **Rich Content Support**: Text, tables, images, flowcharts, equations (LaTeX)
- **Flexible Structure**: Add, remove, reorder sections dynamically
- **Real-time Preview**: See your document as you build it

### 🔐 **Collaboration & Version Control**
- **Role-Based Access**: Doer, Reviewer, Approver, Admin
- **Version History**: Full audit trail of all changes
- **Document Approval**: Lock documents after approval
- **User Tracking**: Track who made what changes and when

### 📤 **Multi-Format Export**
- **Word (DOCX)**: Professional formatting with tables and styles
- **PDF**: Print-ready documents
- **HTML**: Web-friendly format with CSS styling
- **Markdown**: Plain text with formatting
- **Excel**: Export tables and checklists

### 📖 **Standards Reference Database**
- Integrated database of 12+ international standards
- Search and filter by category, organization, keyword
- Auto-citations in Normative References sections
- Easy standard selection during document creation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) wkhtmltopdf for PDF export

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sop-gen.git
   cd sop-gen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys (Optional for AI features)**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```bash
   OPENAI_API_KEY=your-openai-key
   ANTHROPIC_API_KEY=your-anthropic-key
   ```

   **Note:** The app works in demo mode without API keys for testing!

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**

   Navigate to `http://localhost:8501`

## 📖 Usage Guide

### Creating Your First SOP

1. **Choose a Starting Point**
   - Select from 10+ industry templates
   - Upload your own custom template
   - Or start from scratch

2. **Fill Document Information**
   - Document title and number
   - Company/organization details
   - Revision and effective date
   - Select applicable standards

3. **Edit Sections**
   - Click "🤖 Generate" to use AI for any section
   - Or type content manually
   - Edit AI-generated content as needed
   - Add/remove sections dynamically

4. **Preview & Export**
   - Review the formatted document
   - Export to DOCX, PDF, HTML, or Excel
   - Save to document library

5. **Approval Workflow**
   - Reviewers can check content
   - Approvers can lock the document
   - Admins can unlock if needed

### Using AI Generation

The AI generator works in two modes:

**Demo Mode (No API Keys)**
- Uses intelligent mock content
- Perfect for testing and evaluation
- No cost, no setup required

**Production Mode (With API Keys)**
- Real AI generation with GPT-4 or Claude
- High-quality, context-aware content
- Automatically routes to best model per section

### Exporting Documents

Click the "Export" tab and choose your format:

- **DOCX**: Full-featured Word document with formatting
- **PDF**: Print-ready PDF (requires wkhtmltopdf or weasyprint)
- **HTML**: Styled web page with CSS
- **Markdown**: Plain text with markdown formatting
- **Excel**: Spreadsheet for tables and checklists

## 🏗️ Architecture

```
sop-gen/
├── app.py                    # Main Streamlit application
├── sopgen/                   # Core package
│   ├── __init__.py
│   ├── models.py            # Data models (Document, Section, Version)
│   ├── templates.py         # Template library management
│   ├── generator.py         # AI content generation engine
│   ├── export.py            # Multi-format export
│   └── utils.py             # Utility functions
├── templates/               # Template JSON files
│   ├── iec_61215.json
│   ├── iso_17025.json
│   └── ...
├── data/                    # Document storage
│   └── documents/
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

### Module Overview

- **models.py**: Core data structures for documents, sections, and versions
- **templates.py**: Template library and standards database management
- **generator.py**: AI content generation with multi-model routing
- **export.py**: Document export to DOCX, PDF, HTML, Excel, Markdown
- **app.py**: Streamlit UI with section editing and preview

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# AI API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Directories
DATA_DIR=data/documents
TEMPLATES_DIR=templates

# User Defaults
DEFAULT_USER=User
DEFAULT_ROLE=doer
```

### Adding Custom Templates

Create a JSON file in the `templates/` directory:

```json
{
  "title": "My Custom SOP",
  "doc_number": "SOP-CUSTOM-001",
  "standard": "Custom",
  "description": "Custom SOP template",
  "metadata": {
    "category": "Custom"
  },
  "sections": [
    {
      "title": "Purpose",
      "content": "",
      "content_type": "text"
    }
  ]
}
```

## 📋 Available Templates

| Template | Standard | Category | Sections |
|----------|----------|----------|----------|
| IEC 61215 | IEC 61215 | Solar PV Testing | 18 |
| IEC 61730 | IEC 61730 | Solar PV Safety | 14 |
| IEC 61853 | IEC 61853 | PV Performance | 15 |
| IEC 62804 | IEC 62804 | PID Testing | 15 |
| ISO 17025 | ISO/IEC 17025 | Lab Testing | 17 |
| ISO 9001 | ISO 9001 | Quality Management | 15 |
| ISO 14001 | ISO 14001 | Environmental | 16 |
| ISO 45001 | ISO 45001 | Health & Safety | 16 |
| ISO 27001 | ISO 27001 | Info Security | 16 |
| Generic SOP | Generic | General | 14 |

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=sopgen tests/
```

### Code Structure

The project follows a modular architecture:

1. **Data Layer** (`models.py`): Core data structures
2. **Business Logic** (`templates.py`, `generator.py`): Template management and AI generation
3. **Export Layer** (`export.py`): Document export functionality
4. **Presentation** (`app.py`): Streamlit UI

### Adding New AI Models

Edit `sopgen/generator.py` and add to `_initialize_model_config()`:

```python
"new_model": {
    "provider": "provider_name",
    "model_name": "model-id",
    "max_tokens": 8000,
    "strengths": ["capability1", "capability2"]
}
```

Then add generation logic in `_generate_new_model()` method.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Anthropic for Claude API
- Streamlit for the amazing framework
- python-docx for Word document generation
- All contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sop-gen/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/sop-gen/wiki)
- **Email**: support@example.com

## 🗺️ Roadmap

- [ ] Real-time collaboration with WebSockets
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] React/Next.js frontend
- [ ] REST API for programmatic access
- [ ] Advanced template designer
- [ ] Equation editor with visual LaTeX input
- [ ] Flowchart designer integration
- [ ] Multi-language support
- [ ] Cloud deployment (AWS, Azure, GCP)
- [ ] Mobile app

## 📊 Status

**Current Version**: 1.0.0
**Status**: Production Ready (MVP)
**Last Updated**: November 2024

---

Made with ❤️ by [Ganesh Gowri](https://github.com/yourusername)
