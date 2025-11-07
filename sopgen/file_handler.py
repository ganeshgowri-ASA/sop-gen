"""
File Handler Module for SOP Generator
Handles file uploads including images, logos, flowcharts, and documents
"""

from PIL import Image
import io
import base64
from typing import Dict, List, Optional, Tuple
import logging
import mimetypes

logger = logging.getLogger(__name__)


class FileUploadHandler:
    """Handles file uploads and processing for SOP documents"""

    # Maximum file sizes (in bytes)
    MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB
    MAX_PDF_SIZE = 5 * 1024 * 1024    # 5 MB

    # Allowed file extensions
    ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf'}

    def __init__(self):
        """Initialize the file handler"""
        self.uploaded_files = {
            'logo': None,
            'equipment_photos': [],
            'flowcharts': [],
            'schematics': []
        }
        logger.info("FileUploadHandler initialized")

    def validate_file(self, uploaded_file, file_type: str = 'image') -> Tuple[bool, str]:
        """
        Validate an uploaded file

        Args:
            uploaded_file: Streamlit uploaded file object
            file_type: Type of file ('image', 'pdf', 'any')

        Returns:
            Tuple of (is_valid, error_message)
        """
        if uploaded_file is None:
            return False, "No file uploaded"

        # Get file extension
        file_name = uploaded_file.name
        file_ext = '.' + file_name.split('.')[-1].lower() if '.' in file_name else ''

        # Check file type
        if file_type == 'image':
            if file_ext not in self.ALLOWED_IMAGE_EXTENSIONS:
                return False, f"Invalid image format. Allowed: {', '.join(self.ALLOWED_IMAGE_EXTENSIONS)}"
        elif file_type == 'pdf':
            if file_ext not in self.ALLOWED_DOCUMENT_EXTENSIONS:
                return False, "Invalid document format. Only PDF allowed."

        # Check file size
        file_size = uploaded_file.size
        if file_type == 'image' and file_size > self.MAX_IMAGE_SIZE:
            return False, f"Image too large. Maximum size: {self.MAX_IMAGE_SIZE / (1024*1024):.1f} MB"
        elif file_type == 'pdf' and file_size > self.MAX_PDF_SIZE:
            return False, f"PDF too large. Maximum size: {self.MAX_PDF_SIZE / (1024*1024):.1f} MB"

        return True, ""

    def process_image(self, uploaded_file, max_width: int = 800) -> Optional[Dict]:
        """
        Process an uploaded image file

        Args:
            uploaded_file: Streamlit uploaded file object
            max_width: Maximum width for resizing (maintains aspect ratio)

        Returns:
            Dictionary with image data or None if processing fails
        """
        try:
            # Read the image
            image_bytes = uploaded_file.read()
            image = Image.open(io.BytesIO(image_bytes))

            # Convert RGBA to RGB if needed
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background

            # Resize if too large
            if image.width > max_width:
                aspect_ratio = image.height / image.width
                new_height = int(max_width * aspect_ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Convert to base64 for embedding
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            return {
                'name': uploaded_file.name,
                'format': image.format or 'PNG',
                'size': uploaded_file.size,
                'width': image.width,
                'height': image.height,
                'base64': img_base64,
                'mime_type': uploaded_file.type or 'image/png'
            }

        except Exception as e:
            logger.error(f"Error processing image {uploaded_file.name}: {str(e)}")
            return None

    def process_logo(self, uploaded_file) -> Optional[Dict]:
        """
        Process a company logo upload

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Dictionary with logo data or None
        """
        is_valid, error_msg = self.validate_file(uploaded_file, 'image')
        if not is_valid:
            logger.error(f"Logo validation failed: {error_msg}")
            return None

        logo_data = self.process_image(uploaded_file, max_width=400)
        if logo_data:
            self.uploaded_files['logo'] = logo_data
            logger.info(f"Logo processed: {logo_data['name']}")

        return logo_data

    def process_equipment_photos(self, uploaded_files: List) -> List[Dict]:
        """
        Process multiple equipment photo uploads

        Args:
            uploaded_files: List of Streamlit uploaded file objects

        Returns:
            List of dictionaries with image data
        """
        processed_photos = []

        for uploaded_file in uploaded_files:
            is_valid, error_msg = self.validate_file(uploaded_file, 'image')
            if not is_valid:
                logger.warning(f"Equipment photo validation failed: {error_msg}")
                continue

            photo_data = self.process_image(uploaded_file, max_width=600)
            if photo_data:
                processed_photos.append(photo_data)
                logger.info(f"Equipment photo processed: {photo_data['name']}")

        self.uploaded_files['equipment_photos'] = processed_photos
        return processed_photos

    def process_flowchart(self, uploaded_file) -> Optional[Dict]:
        """
        Process a flowchart or schematic upload

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Dictionary with flowchart data or None
        """
        # Check if it's an image or PDF
        file_ext = '.' + uploaded_file.name.split('.')[-1].lower()

        if file_ext in self.ALLOWED_IMAGE_EXTENSIONS:
            is_valid, error_msg = self.validate_file(uploaded_file, 'image')
            if not is_valid:
                logger.error(f"Flowchart validation failed: {error_msg}")
                return None

            flowchart_data = self.process_image(uploaded_file, max_width=800)
            if flowchart_data:
                self.uploaded_files['flowcharts'].append(flowchart_data)
                logger.info(f"Flowchart processed: {flowchart_data['name']}")

            return flowchart_data

        elif file_ext in self.ALLOWED_DOCUMENT_EXTENSIONS:
            is_valid, error_msg = self.validate_file(uploaded_file, 'pdf')
            if not is_valid:
                logger.error(f"Flowchart PDF validation failed: {error_msg}")
                return None

            # For PDFs, just store the raw data
            pdf_bytes = uploaded_file.read()
            pdf_data = {
                'name': uploaded_file.name,
                'format': 'PDF',
                'size': uploaded_file.size,
                'data': pdf_bytes,
                'mime_type': 'application/pdf'
            }

            self.uploaded_files['flowcharts'].append(pdf_data)
            logger.info(f"Flowchart PDF processed: {pdf_data['name']}")

            return pdf_data

        return None

    def get_uploaded_files(self) -> Dict:
        """
        Get all uploaded files

        Returns:
            Dictionary with all uploaded files
        """
        return self.uploaded_files

    def clear_uploads(self, category: Optional[str] = None):
        """
        Clear uploaded files

        Args:
            category: Specific category to clear ('logo', 'equipment_photos', 'flowcharts')
                     If None, clears all uploads
        """
        if category:
            if category in self.uploaded_files:
                if isinstance(self.uploaded_files[category], list):
                    self.uploaded_files[category] = []
                else:
                    self.uploaded_files[category] = None
                logger.info(f"Cleared uploads for category: {category}")
        else:
            self.uploaded_files = {
                'logo': None,
                'equipment_photos': [],
                'flowcharts': [],
                'schematics': []
            }
            logger.info("Cleared all uploads")

    def add_images_to_document(self, document) -> 'Document':
        """
        Add uploaded images to a document object

        Args:
            document: Document object to add images to

        Returns:
            Modified document object
        """
        # Add logo to metadata
        if self.uploaded_files['logo']:
            document.metadata['company_logo'] = self.uploaded_files['logo']

        # Add equipment photos to metadata
        if self.uploaded_files['equipment_photos']:
            document.metadata['equipment_photos'] = self.uploaded_files['equipment_photos']

        # Add flowcharts to metadata
        if self.uploaded_files['flowcharts']:
            document.metadata['flowcharts'] = self.uploaded_files['flowcharts']

        logger.info(f"Added {len(self.uploaded_files['equipment_photos'])} photos and "
                   f"{len(self.uploaded_files['flowcharts'])} flowcharts to document")

        return document

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"


# Convenience functions
def validate_image_upload(uploaded_file) -> Tuple[bool, str]:
    """
    Quick validation for image uploads

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        Tuple of (is_valid, error_message)
    """
    handler = FileUploadHandler()
    return handler.validate_file(uploaded_file, 'image')


def process_uploaded_image(uploaded_file, max_width: int = 800) -> Optional[Dict]:
    """
    Quick processing for image uploads

    Args:
        uploaded_file: Streamlit uploaded file object
        max_width: Maximum width for resizing

    Returns:
        Dictionary with image data or None
    """
    handler = FileUploadHandler()
    return handler.process_image(uploaded_file, max_width)
