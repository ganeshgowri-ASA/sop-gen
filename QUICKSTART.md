# 🚀 Quick Start Guide - SOP-gen

## Immediate Testing (No Setup Required!)

The application works **immediately in demo mode** without any API keys! You can test all features with mock AI responses.

### 1. Install Dependencies

```bash
pip install streamlit python-docx markdown2 xlsxwriter python-dateutil python-dotenv
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Open Your Browser

Navigate to: `http://localhost:8501`

That's it! You're ready to create SOPs! 🎉

---

## What You Can Do Right Now (Demo Mode)

✅ **Choose from 10+ Templates**
- IEC 61215, 61730, 61853, 62804 (Solar PV)
- ISO 9001, 14001, 17025, 27001, 45001
- Generic SOP

✅ **Create Documents**
- Section-by-section editing
- AI content generation (mock mode)
- Real-time preview

✅ **Export Documents**
- DOCX (Word) - ✅ Works
- HTML - ✅ Works
- Markdown - ✅ Works
- PDF - ⚠️ Requires wkhtmltopdf or weasyprint
- Excel - ✅ Works for tables

✅ **Version Control**
- Track all changes
- User roles and permissions
- Approval workflow

---

## Enable Real AI (Optional)

To use real AI models (GPT-4 or Claude), add your API keys:

### Option 1: Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Option 2: .env File

Create a file named `.env` in the project root:

```bash
cp .env.example .env
# Edit .env and add your keys
```

Then restart the app:

```bash
streamlit run app.py
```

---

## Testing Workflow

### Test 1: Create SOP from Template

1. Click **"Create SOP"** in sidebar
2. Select **"Use Template Library"**
3. Choose **"IEC 61215"**
4. Click **"Load Template"**
5. Fill in document info
6. Click **"Generate with AI"** on any section
7. Preview and export!

### Test 2: AI Content Generation

1. Create or load a document
2. Go to any section
3. Click **"🤖 Generate"**
4. Wait for AI to generate content
5. Edit the generated content as needed
6. Click **"Generate"** again to regenerate

### Test 3: Export to Multiple Formats

1. Go to **"Preview & Export"** tab
2. Select **"Export"** tab
3. Choose format (try DOCX first)
4. Click **"Generate Download"**
5. Download and open the file

### Test 4: Version Control

1. Make changes to sections
2. Go to **"Version History"** tab
3. See all changes logged
4. Each version shows user, timestamp, and changes

### Test 5: Approval Workflow

1. In Settings, set your role to **"approver"**
2. Go to document export tab
3. Click **"Approve & Lock Document"**
4. Try to edit - sections are now locked!
5. Change role to **"admin"** to unlock

---

## Troubleshooting

### Issue: PDF Export Not Working

**Solution 1: Install wkhtmltopdf**
```bash
# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# macOS
brew install wkhtmltopdf

# Windows - Download from: https://wkhtmltopdf.org/downloads.html
```

**Solution 2: Install weasyprint**
```bash
pip install weasyprint
```

**Workaround:** Use HTML or DOCX export, then convert to PDF in Word/Browser

### Issue: Import Errors

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: AI Not Generating Content

**Check:**
1. Are you in demo mode? (It still works, just uses mock content)
2. If using real API: Check API keys are set correctly
3. Check internet connection

### Issue: Templates Not Loading

**Solution:**
```bash
# Check templates directory exists
ls templates/

# Should show 10 JSON files
```

---

## Sample Workflows

### Workflow 1: Quality Management SOP (ISO 9001)

```
1. Create SOP → Use Template Library → iso_9001
2. Edit document info:
   - Title: "Document Control Procedure"
   - Doc Number: SOP-QMS-001
   - Company: Your Company Name
3. Generate sections:
   - Purpose
   - Scope
   - Procedure
4. Export to DOCX
```

### Workflow 2: Solar PV Testing SOP (IEC 61215)

```
1. Create SOP → Use Template Library → iec_61215
2. Edit document info:
   - Title: "Thermal Cycling Test Procedure"
   - Standards: Select IEC 61215
3. Generate all sections with AI
4. Review and edit as needed
5. Export to PDF
```

### Workflow 3: Custom SOP from Scratch

```
1. Create SOP → Start from Scratch
2. Enter title: "Custom Laboratory Procedure"
3. Add custom sections using "➕ Add Section"
4. Generate content for each section
5. Reorder sections by editing section numbers
6. Export to DOCX
```

---

## Features to Explore

### 1. Template Library Page
- View all available templates
- Preview template structures
- Load templates with one click

### 2. Standards Reference Page
- Browse 12+ international standards
- Search by keyword
- See full standard descriptions
- Use in Normative References sections

### 3. Settings Page
- Check AI configuration status
- View system information
- Reset current document

---

## Next Steps

After testing the basic functionality:

1. **Add Real API Keys** for production-quality AI generation
2. **Customize Templates** by editing JSON files in `templates/`
3. **Create Custom Workflows** for your team
4. **Export and Share** SOPs with your organization
5. **Integrate with Your Systems** (future: REST API)

---

## Support & Documentation

- **Full Documentation**: See `README_NEW.md`
- **Code Reference**: Check inline comments in Python files
- **Templates**: Explore `templates/` directory
- **Examples**: All templates are working examples

---

## Performance Tips

1. **Generate One Section at a Time** for better control
2. **Save Frequently** using "Save to Library"
3. **Use Templates** as starting points
4. **Export Early** to test formatting
5. **Version Control** - make changes incrementally

---

## What's Included

✅ **21 Files Created**
- 7 Python modules
- 10 Template JSON files
- 4 Configuration/documentation files

✅ **Full Feature Set**
- AI generation with 3 models (GPT-4, Claude, Mock)
- 10+ industry-standard templates
- 5 export formats
- Version control system
- Role-based access
- Standards database
- Complete UI with 5 pages

✅ **Production Ready**
- Error handling
- Input validation
- Clean architecture
- Comprehensive documentation

---

## Getting Help

**Demo Works But AI Doesn't Generate Quality Content?**
→ You're in mock mode! Add API keys for real AI.

**Can't Export to PDF?**
→ Install wkhtmltopdf or weasyprint, or use DOCX/HTML export.

**Want to Add More Templates?**
→ Copy any JSON file in `templates/` and modify it.

**Need Different Sections?**
→ Use "Add Section" button or edit template JSON.

**Want to Customize AI Prompts?**
→ Edit `sopgen/generator.py` → `_initialize_prompt_templates()`

---

## Success Criteria

You'll know everything is working when you can:

1. ✅ Run `streamlit run app.py` without errors
2. ✅ See 10 templates in Template Library
3. ✅ Create a new SOP from template
4. ✅ Generate content with AI (mock or real)
5. ✅ Export to DOCX and open in Word
6. ✅ See version history with changes

---

**Enjoy using SOP-gen! 🎉**

For issues or questions, check the main README or open a GitHub issue.
