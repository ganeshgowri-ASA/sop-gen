# 🧪 Testing Instructions for SOP-gen

## ✅ Everything is Ready on GitHub!

All code has been committed and pushed to your branch:
**`claude/sop-gen-ai-document-generator-011CUrXV9eKQxaS2JXtqYYkt`**

🔗 **View on GitHub**: https://github.com/ganeshgowri-ASA/sop-gen/tree/claude/sop-gen-ai-document-generator-011CUrXV9eKQxaS2JXtqYYkt

---

## 🚀 Quick Test (3 Steps)

### Step 1: Install Dependencies
```bash
pip install streamlit python-docx markdown2 xlsxwriter python-dateutil python-dotenv
```

### Step 2: Run the App
```bash
streamlit run app.py
```

### Step 3: Open Browser
Go to: **http://localhost:8501**

**That's it!** The app runs in demo mode - no API keys needed for initial testing.

---

## 📁 What Was Built

### Complete File Structure
```
sop-gen/
├── app.py                          # Main Streamlit UI (24KB, 580+ lines)
├── requirements.txt                # All dependencies
├── .env.example                    # API key template
├── .gitignore                      # Git ignore rules
├── QUICKSTART.md                   # Detailed quick start
├── README_NEW.md                   # Full documentation
├── test_setup.py                   # Setup verification script
│
├── sopgen/                         # Core package
│   ├── __init__.py                # Package initialization
│   ├── models.py                  # Document/Section/Version models
│   ├── templates.py               # Template & standards management
│   ├── generator.py               # AI content generation
│   ├── export.py                  # Multi-format export
│   └── utils.py                   # Utility functions
│
├── templates/                      # 10 SOP templates
│   ├── generic_sop.json
│   ├── iec_61215.json            # Solar PV testing
│   ├── iec_61730.json            # PV safety
│   ├── iec_61853.json            # PV performance
│   ├── iec_62804.json            # PID testing
│   ├── iso_17025.json            # Lab testing
│   ├── iso_9001.json             # Quality management
│   ├── iso_14001.json            # Environmental
│   ├── iso_45001.json            # Health & safety
│   └── iso_27001.json            # Info security
│
└── data/                          # Document storage
    └── documents/
```

### Code Statistics
- **Total Files**: 23
- **Python Modules**: 7
- **Templates**: 10
- **Documentation**: 3
- **Total Lines of Code**: ~3,500+

---

## 🧪 Testing Checklist

### ✅ Test 1: Verify Setup (30 seconds)
```bash
python3 test_setup.py
```
**Expected**: 5/6 tests pass (Streamlit may not be installed yet)

### ✅ Test 2: Run App (1 minute)
```bash
streamlit run app.py
```
**Expected**: Browser opens to http://localhost:8501

### ✅ Test 3: Load Template (2 minutes)
1. Click **"📄 Create SOP"** in sidebar
2. Select **"📚 Use Template Library"**
3. Choose **"iec_61215"** from dropdown
4. Click **"📋 Load Template"**
5. **Expected**: Document created with 18 sections

### ✅ Test 4: AI Generation (2 minutes)
1. In any section, click **"🤖 Generate"**
2. Wait 1-2 seconds
3. **Expected**: Mock content appears (professional-looking text)
4. Try editing the content
5. **Expected**: Changes are saved

### ✅ Test 5: Export DOCX (1 minute)
1. Go to **"👀 Step 4: Preview & Export"**
2. Click **"Export"** tab
3. Select **"DOCX (Word)"**
4. Click **"📥 Generate Download"**
5. Download and open in Word
6. **Expected**: Professional SOP document

### ✅ Test 6: Browse Templates (1 minute)
1. Click **"📚 Template Library"** in sidebar
2. **Expected**: See 10 templates displayed
3. Click preview on any template
4. **Expected**: See section list

### ✅ Test 7: Standards Database (1 minute)
1. Click **"📖 Standards Reference"** in sidebar
2. **Expected**: See 12+ standards organized by category
3. Search for "IEC"
4. **Expected**: 4 IEC standards shown

---

## 🤖 Testing with Real AI (Optional)

### Enable OpenAI GPT-4

1. **Get API Key**: https://platform.openai.com/api-keys

2. **Set Environment Variable**:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Or Create .env File**:
   ```bash
   echo "OPENAI_API_KEY=sk-your-key-here" > .env
   ```

4. **Restart App**:
   ```bash
   streamlit run app.py
   ```

5. **Verify**: Go to Settings page, should show "✅ OpenAI API Key: Configured"

6. **Test**: Generate any section - content will be much more detailed and contextual

### Enable Anthropic Claude

Same process, but use:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

---

## 📊 Expected Results

### Demo Mode (No API Keys)
- ✅ All features work
- ✅ AI generates professional mock content
- ✅ Content is realistic and well-formatted
- ✅ Perfect for UI/UX testing
- ✅ No cost, instant responses

### Production Mode (With API Keys)
- ✅ Real AI-powered generation
- ✅ Context-aware content
- ✅ Adapts to your specific SOP title
- ✅ References selected standards
- ✅ High-quality, ready-to-use text

---

## 🎯 Key Features to Test

### 1. Template System
- **Load template**: Instant SOP structure
- **Preview**: See sections before loading
- **Metadata**: Standard, category, description

### 2. AI Generation
- **Section-by-section**: Generate any section independently
- **Smart routing**: Different AI models for different sections
- **Editable**: Modify AI-generated content
- **Regenerate**: Click generate again for new content

### 3. Document Editing
- **Add sections**: Custom sections anytime
- **Remove sections**: Delete unwanted sections
- **Reorder**: Change section order
- **Rich editing**: Text areas for all content

### 4. Export Formats
- **DOCX**: Professional Word document
- **PDF**: Requires wkhtmltopdf (optional)
- **HTML**: Styled web page
- **Markdown**: Plain text with formatting
- **Excel**: Tables and checklists

### 5. Version Control
- **Auto-logging**: Every change tracked
- **User tracking**: Who made changes
- **Timestamp**: When changes occurred
- **Snapshot**: Full document state per version

### 6. Approval Workflow
- **Roles**: Doer, Reviewer, Approver, Admin
- **Lock**: Prevent edits after approval
- **Unlock**: Admin can reopen documents
- **Audit trail**: All approvals logged

---

## 🐛 Known Limitations

1. **PDF Export**: Requires wkhtmltopdf or weasyprint installed
   - **Workaround**: Export to DOCX, then save as PDF from Word

2. **Real-time Collaboration**: Not implemented in MVP
   - **Current**: Sequential editing only

3. **Image Upload**: Basic file path support only
   - **Future**: Direct image upload and embedding

4. **Flowchart Designer**: Text input only
   - **Future**: Visual flowchart editor

---

## 💡 Pro Tips

### Tip 1: Test in Order
1. First: Load a template
2. Second: Generate 2-3 sections
3. Third: Export to DOCX
4. Fourth: Try other features

### Tip 2: Use Demo Mode Initially
- No setup needed
- Test all UI features
- Understand workflow
- Then add API keys

### Tip 3: Check Version History
- After making changes
- Go to "Version History" tab
- See all logged changes
- Understand audit trail

### Tip 4: Try Different Templates
- Each has different sections
- Some are test-focused (IEC)
- Some are management-focused (ISO)
- Generic works for anything

### Tip 5: Export Multiple Formats
- Try DOCX first (most reliable)
- Then HTML (always works)
- Then Markdown (simple)
- PDF last (requires extra tools)

---

## 🎓 Learning Path

### Beginner (10 minutes)
1. Run app
2. Load one template
3. Generate 2 sections
4. Export to DOCX

### Intermediate (30 minutes)
1. Try all 10 templates
2. Generate full document
3. Edit AI content
4. Test all export formats
5. Check version history

### Advanced (1 hour)
1. Add API keys
2. Compare mock vs real AI
3. Create custom template
4. Test approval workflow
5. Modify prompt templates in code

---

## 📸 Screenshots to Verify

### Home Page
- Should see: Welcome message, 3 feature boxes, 10 features listed
- Navigation: 5 menu items in sidebar

### Create SOP Page
- Should see: Template selection, document info form, section editors
- Each section: Title, Generate button, Clear button, Remove button

### Template Library Page
- Should see: 10 template cards in 3 columns
- Each card: Title, standard, section count

### Standards Reference Page
- Should see: Categories (Solar PV, Quality Management, etc.)
- Each standard: Full name, organization, description

### Settings Page
- Should see: API key status, system info, reset button
- Demo mode warning if no API keys

---

## ✨ Success Criteria

**You'll know it's working when you can:**

1. ✅ App starts without errors
2. ✅ See 10 templates available
3. ✅ Load a template successfully
4. ✅ Generate section content (mock or real)
5. ✅ Edit generated content
6. ✅ Export to DOCX and open in Word
7. ✅ See professional-looking SOP document
8. ✅ Navigate all 5 pages without errors

---

## 🆘 If Something Doesn't Work

### Problem: Import errors
**Solution**: `pip install -r requirements.txt`

### Problem: Can't run streamlit
**Solution**: `pip install streamlit`

### Problem: No templates showing
**Solution**: Check `templates/` directory exists with JSON files

### Problem: AI not generating
**Solution**: Check if in demo mode (Settings page) - it still works!

### Problem: Export fails
**Solution**: Try different format (DOCX first, then HTML)

### Problem: App crashes
**Solution**: Check terminal for error messages, verify Python 3.8+

---

## 📞 Support

**Repository**: https://github.com/ganeshgowri-ASA/sop-gen
**Branch**: `claude/sop-gen-ai-document-generator-011CUrXV9eKQxaS2JXtqYYkt`

**Documentation Files**:
- `QUICKSTART.md` - Quick start guide
- `README_NEW.md` - Full documentation
- `TESTING_INSTRUCTIONS.md` - This file
- `.env.example` - API key template

---

## 🎉 Ready to Test!

```bash
# Quick start:
cd sop-gen
pip install streamlit python-docx markdown2 xlsxwriter
streamlit run app.py

# Open: http://localhost:8501
# Click: Create SOP → Use Template Library → iec_61215
# Click: Generate on any section
# Click: Export → DOCX
# Done! 🎊
```

**Happy Testing! 🚀**
