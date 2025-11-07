"""
Translation Module for SOP Generator
Supports multi-language translation for generated SOPs
"""

from deep_translator import GoogleTranslator
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentTranslator:
    """Handles translation of SOP documents to multiple languages"""

    # Supported languages with their codes
    SUPPORTED_LANGUAGES = {
        # Indian Languages
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Gujarati": "gu",
        "Marathi": "mr",
        "Bengali": "bn",

        # International Languages
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Arabic": "ar",
        "Chinese (Simplified)": "zh-CN",
        "Japanese": "ja",

        # Default
        "English": "en"
    }

    def __init__(self):
        """Initialize the translator"""
        self.available_languages = list(self.SUPPORTED_LANGUAGES.keys())
        logger.info(f"DocumentTranslator initialized with {len(self.available_languages)} languages")

    def get_language_code(self, language_name: str) -> str:
        """
        Get the language code for a given language name

        Args:
            language_name: Name of the language (e.g., "Hindi", "Spanish")

        Returns:
            Language code (e.g., "hi", "es")
        """
        return self.SUPPORTED_LANGUAGES.get(language_name, "en")

    def translate_text(self, text: str, target_language: str, source_language: str = "en") -> str:
        """
        Translate a single text string

        Args:
            text: Text to translate
            target_language: Target language name or code
            source_language: Source language code (default: "en")

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text

        # Convert language name to code if needed
        if target_language in self.SUPPORTED_LANGUAGES:
            target_code = self.SUPPORTED_LANGUAGES[target_language]
        else:
            target_code = target_language

        # Skip translation if target is English
        if target_code == "en":
            return text

        try:
            translator = GoogleTranslator(source=source_language, target=target_code)

            # Handle long text by splitting into chunks (Google Translator has a 5000 char limit)
            max_length = 4500
            if len(text) <= max_length:
                return translator.translate(text)
            else:
                # Split by paragraphs and translate
                chunks = self._split_text(text, max_length)
                translated_chunks = []
                for chunk in chunks:
                    if chunk.strip():
                        translated_chunks.append(translator.translate(chunk))
                    else:
                        translated_chunks.append(chunk)
                return "\n\n".join(translated_chunks)

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return f"[Translation Error: {text[:100]}...]"

    def _split_text(self, text: str, max_length: int) -> List[str]:
        """
        Split text into chunks at paragraph boundaries

        Args:
            text: Text to split
            max_length: Maximum length of each chunk

        Returns:
            List of text chunks
        """
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 <= max_length:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def translate_document(self, document, target_language: str) -> 'Document':
        """
        Translate an entire SOP document

        Args:
            document: Document object to translate
            target_language: Target language name (e.g., "Hindi", "Spanish")

        Returns:
            Translated document object
        """
        from sopgen.models import Document, Section
        import copy

        # Create a copy of the document
        translated_doc = copy.deepcopy(document)

        logger.info(f"Translating document to {target_language}")

        # Translate metadata
        if "title" in translated_doc.metadata:
            translated_doc.metadata["title"] = self.translate_text(
                translated_doc.metadata["title"],
                target_language
            )

        if "company" in translated_doc.metadata:
            translated_doc.metadata["company"] = self.translate_text(
                translated_doc.metadata["company"],
                target_language
            )

        # Add language marker to metadata
        translated_doc.metadata["translated_to"] = target_language
        translated_doc.metadata["original_language"] = "English"

        # Translate all sections
        for section in translated_doc.sections:
            # Translate section title
            section.title = self.translate_text(section.title, target_language)

            # Translate section content
            if section.content:
                section.content = self.translate_text(section.content, target_language)

            # Mark as translated
            section.metadata["translated"] = True
            section.metadata["language"] = target_language

        logger.info(f"Document translation completed: {len(translated_doc.sections)} sections translated")

        return translated_doc

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language names

        Returns:
            List of language names
        """
        return self.available_languages

    def translate_section_content(self, section, target_language: str) -> str:
        """
        Translate a single section's content

        Args:
            section: Section object
            target_language: Target language name

        Returns:
            Translated content
        """
        if not section.content:
            return ""

        return self.translate_text(section.content, target_language)


# Convenience function for quick translations
def translate(text: str, to_language: str, from_language: str = "en") -> str:
    """
    Quick translation function

    Args:
        text: Text to translate
        to_language: Target language
        from_language: Source language (default: "en")

    Returns:
        Translated text
    """
    translator = DocumentTranslator()
    return translator.translate_text(text, to_language, from_language)
