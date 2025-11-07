"""
SOP-gen: AI-Powered SOP Document Generator
Main Streamlit Application
"""

import streamlit as st
from datetime import datetime
import os
import sys

# Add sopgen to path
sys.path.insert(0, os.path.dirname(__file__))

from sopgen.models import Document, Section
from sopgen.templates import TemplateManager, StandardsManager
from sopgen.generator import AIContentGenerator
from sopgen.export import DocumentExporter
from sopgen.utils import sanitize_filename, generate_doc_number

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="SOP-gen: AI Document Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #004E89;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF6B35;
        margin: 15px 0;
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #cce5ff;
        border-left: 5px solid #004085;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #FF6B35;
        color: white;
        border-radius: 5px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #E65A2E;
        border: 2px solid #004E89;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'current_doc' not in st.session_state:
    st.session_state.current_doc = None

if 'ai_generator' not in st.session_state:
    st.session_state.ai_generator = AIContentGenerator()

if 'template_manager' not in st.session_state:
    st.session_state.template_manager = TemplateManager()

if 'standards_manager' not in st.session_state:
    st.session_state.standards_manager = StandardsManager()

if 'exporter' not in st.session_state:
    st.session_state.exporter = DocumentExporter()

if 'current_user' not in st.session_state:
    st.session_state.current_user = "User"

if 'current_role' not in st.session_state:
    st.session_state.current_role = "doer"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 📝 SOP-gen")
    st.markdown("*AI-Powered Document Generator*")
    st.markdown("---")

    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📄 Create SOP", "📚 Template Library", "📖 Standards Reference", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # User info (simple version for MVP)
    st.markdown("### 👤 User Information")
    st.session_state.current_user = st.text_input("Your Name", value=st.session_state.current_user)
    st.session_state.current_role = st.selectbox(
        "Your Role",
        ["doer", "reviewer", "approver", "admin"],
        index=["doer", "reviewer", "approver", "admin"].index(st.session_state.current_role)
    )

    st.markdown("---")

    # AI Status
    st.markdown("### 🤖 AI Status")
    if st.session_state.ai_generator.use_mock:
        st.warning("⚠️ Running in Demo Mode\n\nAdd API keys for real AI generation")
    else:
        st.success("✅ AI Models Active")

    st.markdown("---")

    # Quick stats
    if st.session_state.current_doc:
        st.markdown("### 📊 Current Document")
        st.info(f"**Sections:** {len(st.session_state.current_doc.sections)}")
        filled = sum(1 for s in st.session_state.current_doc.sections if s.content.strip())
        st.info(f"**Filled:** {filled}/{len(st.session_state.current_doc.sections)}")

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.markdown('<p class="main-header">📝 SOP-gen: AI-Powered SOP Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate Professional Standard Operating Procedures in Minutes</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="section-box">
        <h3>🚀 Quick Start</h3>
        <p>Choose from 10+ industry-standard templates or create custom SOPs from scratch</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-box">
        <h3>🤖 AI-Powered</h3>
        <p>Intelligent content generation with GPT-4 and Claude AI models</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="section-box">
        <h3>📤 Multi-Format Export</h3>
        <p>Export to DOCX, PDF, HTML, and Excel with one click</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ✨ Key Features")
    features_col1, features_col2 = st.columns(2)

    with features_col1:
        st.markdown("""
        - ✅ **10+ Industry Templates** (IEC, ISO, ASTM standards)
        - ✅ **AI Content Generation** with smart routing
        - ✅ **Section-by-Section Editing** for precision
        - ✅ **Version Control** with full audit trail
        - ✅ **Multi-Format Export** (DOCX, PDF, HTML, Excel)
        """)

    with features_col2:
        st.markdown("""
        - ✅ **Role-Based Access** (Doer, Reviewer, Approver, Admin)
        - ✅ **Document Approval** workflow with locking
        - ✅ **Standards Database** with auto-citations
        - ✅ **Rich Content Support** (text, tables, images, equations)
        - ✅ **Template Library** management
        """)

    st.markdown("---")

    st.markdown('<div class="success-box">👉 Click <b>"Create SOP"</b> in the sidebar to get started!</div>', unsafe_allow_html=True)

    # Available templates showcase
    st.markdown("### 📚 Available Templates")
    templates = st.session_state.template_manager.list_templates()

    template_cols = st.columns(4)
    for idx, template in enumerate(templates):
        with template_cols[idx % 4]:
            st.markdown(f"**{template.replace('_', ' ').title()}**")

# ==================== CREATE SOP PAGE ====================
elif page == "📄 Create SOP":
    st.markdown('<p class="main-header">📄 Create New SOP</p>', unsafe_allow_html=True)

    # Step 1: Template Selection
    st.markdown("## 🗂️ Step 1: Choose Starting Point")

    template_option = st.radio(
        "How would you like to start?",
        ["🆕 Start from Scratch", "📚 Use Template Library", "📤 Upload Custom Template"],
        horizontal=True
    )

    selected_template_name = None

    if template_option == "📚 Use Template Library":
        templates = st.session_state.template_manager.list_templates()

        col1, col2 = st.columns([3, 1])

        with col1:
            selected_template_name = st.selectbox(
                "Select a template:",
                templates,
                format_func=lambda x: x.replace('_', ' ').title()
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📋 Load Template", use_container_width=True):
                try:
                    doc = st.session_state.template_manager.load_template(selected_template_name)
                    st.session_state.current_doc = doc
                    st.success(f"✅ Template '{selected_template_name}' loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error loading template: {e}")

        # Show template preview
        if selected_template_name:
            with st.expander("👀 Preview Template Structure"):
                info = st.session_state.template_manager.get_template_info(selected_template_name)
                if info:
                    st.write(f"**Standard:** {info['standard']}")
                    st.write(f"**Description:** {info['description']}")
                    st.write(f"**Sections ({info['section_count']}):**")
                    for section in info['sections']:
                        st.write(f"  • {section}")

    elif template_option == "🆕 Start from Scratch":
        col1, col2 = st.columns([3, 1])

        with col1:
            new_doc_title = st.text_input("Document Title", placeholder="e.g., Thermal Cycling Test Procedure")

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ Create New Document", use_container_width=True):
                if new_doc_title:
                    doc = Document(
                        title=new_doc_title,
                        doc_number=generate_doc_number("SOP"),
                        created_by=st.session_state.current_user
                    )
                    # Add basic sections
                    basic_sections = [
                        "Purpose", "Scope", "Definitions and Abbreviations",
                        "Responsibilities", "References", "Procedure",
                        "Safety Considerations", "Records"
                    ]
                    for idx, section_title in enumerate(basic_sections):
                        doc.add_section(section_title, order=idx)

                    st.session_state.current_doc = doc
                    st.success(f"✅ New document created: {new_doc_title}")
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter a document title")

    # Step 2: Document Metadata
    if st.session_state.current_doc:
        st.markdown("---")
        st.markdown("## 📋 Step 2: Document Information")

        doc = st.session_state.current_doc

        col1, col2, col3 = st.columns(3)

        with col1:
            doc.title = st.text_input("SOP Title*", value=doc.title)
            doc.doc_number = st.text_input("Document Number*", value=doc.doc_number or generate_doc_number("SOP"))

        with col2:
            if 'company' not in doc.metadata:
                doc.metadata['company'] = ""
            doc.metadata['company'] = st.text_input("Company/Organization", value=doc.metadata.get('company', ''))

            if 'revision' not in doc.metadata:
                doc.metadata['revision'] = "Rev 1.0"
            doc.metadata['revision'] = st.text_input("Revision", value=doc.metadata.get('revision', 'Rev 1.0'))

        with col3:
            if 'effective_date' not in doc.metadata:
                doc.metadata['effective_date'] = datetime.now().strftime('%Y-%m-%d')

            effective_date = st.date_input("Effective Date", value=datetime.now())
            doc.metadata['effective_date'] = effective_date.strftime('%Y-%m-%d')

            # Standards selection
            all_standards = list(st.session_state.standards_manager.get_all_standards().keys())
            selected_standards = st.multiselect(
                "Applicable Standards",
                all_standards,
                default=doc.metadata.get('standards', []) if isinstance(doc.metadata.get('standards'), list) else []
            )
            doc.metadata['standards'] = selected_standards

        # File Upload Section
        st.markdown("---")
        st.markdown("### 📎 File Uploads")

        # Initialize file handler in session state
        if 'file_handler' not in st.session_state:
            from sopgen.file_handler import FileUploadHandler
            st.session_state.file_handler = FileUploadHandler()

        upload_col1, upload_col2, upload_col3 = st.columns(3)

        with upload_col1:
            st.markdown("#### 🏢 Company Logo")
            logo_file = st.file_uploader(
                "Upload Logo (PNG/JPG, max 2MB)",
                type=['png', 'jpg', 'jpeg'],
                key="logo_upload",
                help="Upload your company logo to appear on the title page"
            )

            if logo_file:
                logo_data = st.session_state.file_handler.process_logo(logo_file)
                if logo_data:
                    st.success(f"✅ Logo uploaded: {logo_data['name']}")
                    st.image(logo_file, width=150)
                else:
                    st.error("❌ Logo upload failed")

        with upload_col2:
            st.markdown("#### 🔧 Equipment Photos")
            equipment_files = st.file_uploader(
                "Upload Equipment Photos (Multiple files)",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True,
                key="equipment_upload",
                help="Upload photos of equipment used in the SOP"
            )

            if equipment_files:
                equipment_data = st.session_state.file_handler.process_equipment_photos(equipment_files)
                if equipment_data:
                    st.success(f"✅ {len(equipment_data)} photos uploaded")
                    # Show thumbnails
                    for i, photo in enumerate(equipment_data[:3]):  # Show max 3 thumbnails
                        if i < len(equipment_files):
                            st.image(equipment_files[i], width=100)
                else:
                    st.error("❌ Photo upload failed")

        with upload_col3:
            st.markdown("#### 📊 Flowchart/Schematic")
            flowchart_file = st.file_uploader(
                "Upload Flowchart (PNG/JPG/PDF)",
                type=['png', 'jpg', 'jpeg', 'pdf'],
                key="flowchart_upload",
                help="Upload process flowcharts or schematics"
            )

            if flowchart_file:
                flowchart_data = st.session_state.file_handler.process_flowchart(flowchart_file)
                if flowchart_data:
                    st.success(f"✅ Flowchart uploaded: {flowchart_data['name']}")
                    if flowchart_data['format'] != 'PDF':
                        st.image(flowchart_file, width=150)
                else:
                    st.error("❌ Flowchart upload failed")

        # Add uploads to document metadata
        if st.button("💾 Attach Files to Document"):
            st.session_state.file_handler.add_images_to_document(doc)
            st.success("✅ Files attached to document!")

        # Step 3: Section Editing
        st.markdown("---")
        st.markdown("## ✍️ Step 3: Edit SOP Sections")

        st.markdown('<div class="info-box">💡 <b>Tip:</b> Click "Generate with AI" to auto-fill sections, or type content manually. You can edit AI-generated content.</div>', unsafe_allow_html=True)

        # Section management
        col_left, col_right = st.columns([1, 4])

        with col_left:
            if st.button("➕ Add Section"):
                new_section_title = f"New Section {len(doc.sections) + 1}"
                doc.add_section(new_section_title)
                st.rerun()

        # Iterate through sections
        for idx, section in enumerate(doc.sections):
            with st.expander(f"📄 {section.title}" + (" ✅" if section.content.strip() else " ⚪"), expanded=not section.content.strip()):

                # Section controls
                col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 1])

                with col_a:
                    # Allow editing section title
                    new_title = st.text_input(
                        f"Section Title",
                        value=section.title,
                        key=f"title_{idx}",
                        label_visibility="collapsed"
                    )
                    if new_title != section.title:
                        section.title = new_title

                with col_b:
                    if st.button("🤖 Generate", key=f"gen_{idx}", help="Generate content with AI"):
                        with st.spinner(f"Generating {section.title}..."):
                            try:
                                generated_content = st.session_state.ai_generator.generate_section_content(
                                    doc, section
                                )
                                section.content = generated_content
                                section.ai_generated = True
                                doc.log_version(
                                    user=st.session_state.current_user,
                                    role=st.session_state.current_role,
                                    changes=f"AI generated content for {section.title}"
                                )
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")

                with col_c:
                    if st.button("🗑️ Clear", key=f"clear_{idx}", help="Clear content"):
                        section.content = ""
                        section.ai_generated = False
                        st.rerun()

                with col_d:
                    if st.button("❌ Remove", key=f"remove_{idx}", help="Remove section"):
                        doc.remove_section(section.title)
                        st.rerun()

                # Content editing
                section_content = st.text_area(
                    f"Content for {section.title}",
                    value=section.content,
                    height=200,
                    key=f"content_{idx}",
                    label_visibility="collapsed"
                )

                # Update content if changed
                if section_content != section.content:
                    section.content = section_content

                # Show if AI-generated
                if section.ai_generated:
                    st.caption("🤖 AI-Generated (you can edit)")

        # Step 4: Preview and Export
        st.markdown("---")
        st.markdown("## 👀 Step 4: Preview & Export")

        tab_preview, tab_export, tab_version = st.tabs(["📄 Preview", "💾 Export", "📜 Version History"])

        with tab_preview:
            st.markdown("### Document Preview")

            # Generate markdown preview
            preview_md = st.session_state.exporter.to_markdown(doc)
            st.markdown(preview_md)

        with tab_export:
            st.markdown("### Export Document")

            col_exp1, col_exp2 = st.columns(2)

            with col_exp1:
                st.markdown("#### 📥 Download Options")

                # Export format selection
                export_format = st.radio(
                    "Select format:",
                    ["DOCX (Word)", "PDF", "HTML", "Markdown", "Excel (Tables)"],
                    horizontal=False
                )

                # Export button
                if st.button("📥 Generate Download", use_container_width=True, type="primary"):
                    try:
                        format_map = {
                            "DOCX (Word)": ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
                            "PDF": ("pdf", "application/pdf", ".pdf"),
                            "HTML": ("html", "text/html", ".html"),
                            "Markdown": ("markdown", "text/markdown", ".md"),
                            "Excel (Tables)": ("excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx")
                        }

                        format_key, mime_type, extension = format_map[export_format]

                        with st.spinner(f"Generating {export_format}..."):
                            export_bytes = st.session_state.exporter.export_document(doc, format_key)

                            filename = sanitize_filename(f"{doc.doc_number}_{doc.title}{extension}")

                            st.download_button(
                                label=f"⬇️ Download {export_format}",
                                data=export_bytes,
                                file_name=filename,
                                mime=mime_type,
                                use_container_width=True
                            )

                            st.success(f"✅ {export_format} ready for download!")

                    except Exception as e:
                        st.error(f"❌ Export error: {e}")

            with col_exp2:
                st.markdown("#### 🌐 Translation")

                # Initialize translator if not exists
                if 'translator' not in st.session_state:
                    from sopgen.translation import DocumentTranslator
                    st.session_state.translator = DocumentTranslator()

                # Language selection for translation
                target_language = st.selectbox(
                    "Translate to:",
                    options=st.session_state.translator.get_supported_languages(),
                    key="export_translate_lang"
                )

                if st.button("🌐 Translate Document", use_container_width=True, type="secondary"):
                    if target_language == "English":
                        st.info("Document is already in English")
                    else:
                        try:
                            with st.spinner(f"Translating to {target_language}..."):
                                translated_doc = st.session_state.translator.translate_document(doc, target_language)
                                st.session_state.current_doc = translated_doc
                                st.success(f"✅ Document translated to {target_language}!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Translation error: {e}")

                st.markdown("---")

                st.markdown("#### 💾 Save Document")

                if st.button("💾 Save to Library", use_container_width=True):
                    try:
                        filepath = doc.save()
                        st.success(f"✅ Document saved: {filepath}")
                    except Exception as e:
                        st.error(f"❌ Save error: {e}")

                st.markdown("---")

                # Approval workflow
                if st.session_state.current_role in ["approver", "admin"]:
                    st.markdown("#### ✔️ Approval")

                    if not doc.approved:
                        if st.button("✅ Approve & Lock Document", use_container_width=True):
                            doc.approve(st.session_state.current_user)
                            st.success(f"✅ Document approved by {st.session_state.current_user}")
                            st.rerun()
                    else:
                        st.info(f"✅ Approved by: {doc.approver}")

                        if st.session_state.current_role == "admin":
                            if st.button("🔓 Unlock for Editing"):
                                doc.approved = False
                                for sec in doc.sections:
                                    sec.locked = False
                                st.success("Document unlocked")
                                st.rerun()

        with tab_version:
            st.markdown("### Version History")

            if doc.versions:
                for version in reversed(doc.versions):
                    with st.expander(f"Version {version.version_id} - {version.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"):
                        st.write(f"**User:** {version.user} ({version.role})")
                        st.write(f"**Changes:** {version.changes}")
                        st.write(f"**Sections:** {len(version.content_snapshot)}")
            else:
                st.info("No version history yet")

# ==================== TEMPLATE LIBRARY PAGE ====================
elif page == "📚 Template Library":
    st.markdown('<p class="main-header">📚 Template Library</p>', unsafe_allow_html=True)

    templates = st.session_state.template_manager.list_templates()

    st.markdown(f"### Available Templates ({len(templates)})")

    # Display templates in grid
    cols = st.columns(3)

    for idx, template_name in enumerate(templates):
        with cols[idx % 3]:
            info = st.session_state.template_manager.get_template_info(template_name)

            if info:
                st.markdown(f"""
                <div class="section-box">
                <h4>{template_name.replace('_', ' ').title()}</h4>
                <p><b>Standard:</b> {info['standard']}</p>
                <p><b>Sections:</b> {info['section_count']}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Load {template_name}", key=f"load_{template_name}"):
                    doc = st.session_state.template_manager.load_template(template_name)
                    st.session_state.current_doc = doc
                    st.success(f"✅ Loaded {template_name}")
                    st.rerun()

# ==================== STANDARDS REFERENCE PAGE ====================
elif page == "📖 Standards Reference":
    st.markdown('<p class="main-header">📖 Standards Reference</p>', unsafe_allow_html=True)

    standards = st.session_state.standards_manager.get_all_standards()

    st.markdown(f"### Available Standards ({len(standards)})")

    # Search
    search_query = st.text_input("🔍 Search standards", placeholder="e.g., IEC, ISO, Solar PV")

    if search_query:
        standards = st.session_state.standards_manager.search_standards(search_query)

    # Group by category
    categories = {}
    for std_id, std_data in standards.items():
        category = std_data['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((std_id, std_data))

    # Display by category
    for category, stds in categories.items():
        with st.expander(f"📂 {category} ({len(stds)} standards)", expanded=True):
            for std_id, std_data in stds:
                st.markdown(f"""
                **{std_id}** - {std_data['organization']}
                {std_data['full_name']}
                *{std_data['description']}*
                """)
                st.markdown("---")

# ==================== SETTINGS PAGE ====================
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)

    st.markdown("## 🤖 AI Configuration")

    st.markdown("""
    Configure AI models for content generation. Set your API keys as environment variables:

    ```bash
    export OPENAI_API_KEY="your-openai-key"
    export ANTHROPIC_API_KEY="your-anthropic-key"
    ```

    Or create a `.env` file in the project root with:
    ```
    OPENAI_API_KEY=your-openai-key
    ANTHROPIC_API_KEY=your-anthropic-key
    ```
    """)

    # Check current status
    openai_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    col1, col2 = st.columns(2)

    with col1:
        if openai_key:
            st.success("✅ OpenAI API Key: Configured")
        else:
            st.warning("⚠️ OpenAI API Key: Not configured")

    with col2:
        if anthropic_key:
            st.success("✅ Anthropic API Key: Configured")
        else:
            st.warning("⚠️ Anthropic API Key: Not configured")

    if not openai_key and not anthropic_key:
        st.info("💡 Running in demo mode with mock AI responses. Add API keys for real AI generation.")

    st.markdown("---")

    st.markdown("## 🌐 Language Settings")

    # Initialize translator in session state if not exists
    if 'translator' not in st.session_state:
        from sopgen.translation import DocumentTranslator
        st.session_state.translator = DocumentTranslator()

    # Language selection
    available_languages = st.session_state.translator.get_supported_languages()

    # Initialize preferred language in session state
    if 'preferred_language' not in st.session_state:
        st.session_state.preferred_language = "English"

    st.session_state.preferred_language = st.selectbox(
        "Default Document Language",
        options=available_languages,
        index=available_languages.index(st.session_state.preferred_language),
        help="Select the default language for document translation"
    )

    st.info(f"📝 Current language: {st.session_state.preferred_language}")

    st.markdown("---")

    st.markdown("## 📊 System Information")

    st.write(f"**Current User:** {st.session_state.current_user}")
    st.write(f"**Current Role:** {st.session_state.current_role}")
    st.write(f"**AI Mode:** {'Demo/Mock' if st.session_state.ai_generator.use_mock else 'Production'}")
    st.write(f"**Templates Available:** {len(st.session_state.template_manager.list_templates())}")
    st.write(f"**Standards Database:** {len(st.session_state.standards_manager.get_all_standards())} standards")

    st.markdown("---")

    st.markdown("## 🔄 Reset")

    if st.button("🔄 Clear Current Document"):
        st.session_state.current_doc = None
        st.success("✅ Current document cleared")
        st.rerun()
