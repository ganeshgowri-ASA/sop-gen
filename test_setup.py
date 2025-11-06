#!/usr/bin/env python3
"""
Quick test script to verify SOP-gen installation
Run: python3 test_setup.py
"""

import sys

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    try:
        from sopgen import Document, Section, TemplateManager, AIContentGenerator, DocumentExporter
        print("  ✅ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_templates():
    """Test template loading"""
    print("\n📚 Testing templates...")
    try:
        from sopgen.templates import TemplateManager
        tm = TemplateManager()
        templates = tm.list_templates()
        print(f"  ✅ Found {len(templates)} templates:")
        for t in templates:
            print(f"     • {t}")
        return True
    except Exception as e:
        print(f"  ❌ Template error: {e}")
        return False

def test_document_creation():
    """Test document creation"""
    print("\n📄 Testing document creation...")
    try:
        from sopgen.models import Document
        doc = Document(title="Test SOP", doc_number="TEST-001")
        doc.add_section("Purpose", content="Test purpose")
        doc.add_section("Scope", content="Test scope")
        print(f"  ✅ Created document with {len(doc.sections)} sections")
        return True
    except Exception as e:
        print(f"  ❌ Document creation error: {e}")
        return False

def test_ai_generator():
    """Test AI generator initialization"""
    print("\n🤖 Testing AI generator...")
    try:
        from sopgen.generator import AIContentGenerator
        gen = AIContentGenerator()
        mode = "Demo Mode" if gen.use_mock else "Production Mode"
        print(f"  ✅ AI Generator initialized in {mode}")
        return True
    except Exception as e:
        print(f"  ❌ AI generator error: {e}")
        return False

def test_export():
    """Test export functionality"""
    print("\n📤 Testing export...")
    try:
        from sopgen.export import DocumentExporter
        from sopgen.models import Document

        exporter = DocumentExporter()
        doc = Document(title="Test Export", doc_number="EXP-001")
        doc.add_section("Test Section", content="Test content")

        # Test markdown export
        md = exporter.to_markdown(doc)
        print(f"  ✅ Markdown export: {len(md)} characters")

        # Test HTML export
        html = exporter.to_html(doc)
        print(f"  ✅ HTML export: {len(html)} characters")

        return True
    except Exception as e:
        print(f"  ❌ Export error: {e}")
        return False

def check_streamlit():
    """Check if Streamlit is installed"""
    print("\n🎨 Checking Streamlit...")
    try:
        import streamlit
        print(f"  ✅ Streamlit {streamlit.__version__} installed")
        return True
    except ImportError:
        print("  ⚠️  Streamlit not installed")
        print("     Install with: pip install streamlit")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 SOP-gen Setup Test")
    print("=" * 60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Templates", test_templates()))
    results.append(("Document Creation", test_document_creation()))
    results.append(("AI Generator", test_ai_generator()))
    results.append(("Export", test_export()))
    results.append(("Streamlit", check_streamlit()))

    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\n  Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Ready to run: streamlit run app.py")
        print("\n📖 Quick Start:")
        print("   1. Run: streamlit run app.py")
        print("   2. Open: http://localhost:8501")
        print("   3. Start creating SOPs!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
