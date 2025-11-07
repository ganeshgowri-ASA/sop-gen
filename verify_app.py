#!/usr/bin/env python3
"""
SOP-gen Application Verification Script
Tests all components and verifies the app is ready to run
"""

import sys
import os
import subprocess

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
        from sopgen.models import Document, Section, DocumentVersion
        from sopgen.templates import TemplateManager, StandardsManager
        from sopgen.generator import AIContentGenerator
        from sopgen.export import DocumentExporter
        from sopgen.utils import sanitize_filename, generate_doc_number
        import streamlit
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

def test_directories():
    """Test required directories exist"""
    print("Testing directory structure...")
    required_dirs = ['templates', 'data/documents', 'sopgen']
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} missing")
            all_exist = False
    return all_exist

def test_templates():
    """Test template loading"""
    print("Testing templates...")
    from sopgen.templates import TemplateManager
    tm = TemplateManager()
    templates = tm.list_templates()
    if templates:
        print(f"  ✓ Found {len(templates)} templates")
        return True
    else:
        print("  ✗ No templates found")
        return False

def test_components():
    """Test core components"""
    print("Testing components...")
    try:
        from sopgen.models import Document
        from sopgen.generator import AIContentGenerator
        from sopgen.export import DocumentExporter

        # Create test document
        doc = Document(title="Test", doc_number="TEST-001")
        doc.add_section("Test Section", "Test content")

        # Test AI generator
        gen = AIContentGenerator()

        # Test exporter
        exporter = DocumentExporter()
        md = exporter.to_markdown(doc)

        print(f"  ✓ All components working")
        return True
    except Exception as e:
        print(f"  ✗ Component error: {e}")
        return False

def test_app_syntax():
    """Test app.py syntax"""
    print("Testing app.py syntax...")
    result = subprocess.run(
        ['python3', '-m', 'py_compile', 'app.py'],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("  ✓ app.py syntax valid")
        return True
    else:
        print(f"  ✗ Syntax error: {result.stderr}")
        return False

def main():
    print("=" * 60)
    print("SOP-gen Application Verification")
    print("=" * 60)
    print()

    tests = [
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("Templates", test_templates),
        ("Components", test_components),
        ("App Syntax", test_app_syntax)
    ]

    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        results.append(test_func())
        print()

    print("=" * 60)
    if all(results):
        print("✓ ALL TESTS PASSED - App is ready!")
        print("\nTo run the app:")
        print("  streamlit run app.py")
        print("\nNote: Running in DEMO MODE (mock AI responses)")
        print("To enable real AI: Add API keys to .env file")
        return 0
    else:
        print("✗ SOME TESTS FAILED - See errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
