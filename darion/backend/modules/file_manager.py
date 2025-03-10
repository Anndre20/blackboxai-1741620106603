import os
import shutil
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any
import mimetypes
import magic  # for better file type detection
from .logger import setup_logger

logger = setup_logger()

class FileManager:
    def __init__(self):
        self.supported_criteria = ['date', 'type', 'size', 'name']
        self.mime = magic.Magic(mime=True)

    def get_file_type(self, file_path: str) -> str:
        """Get the file type using magic numbers for accurate detection."""
        try:
            return self.mime.from_file(file_path)
        except Exception:
            return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

    def get_file_category(self, mime_type: str) -> str:
        """Categorize file based on MIME type."""
        categories = {
            'image': ['image/'],
            'document': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument'],
            'spreadsheet': ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml'],
            'presentation': ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml'],
            'archive': ['application/zip', 'application/x-rar-compressed', 'application/x-tar'],
            'text': ['text/'],
            'video': ['video/'],
            'audio': ['audio/']
        }
        
        for category, types in categories.items():
            if any(mime_type.startswith(t) for t in types):
                return category
        return 'other'

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get comprehensive file information."""
        try:
            stat = os.stat(file_path)
            mime_type = self.get_file_type(file_path)
            
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'mime_type': mime_type,
                'category': self.get_file_category(mime_type)
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return None

    def sort_files(self, source_dir: str, dest_dir: str, criteria: str = 'type', recursive: bool = True) -> Dict[str, Any]:
        """
        Sort files based on specified criteria.
        
        Args:
            source_dir: Source directory containing files to sort
            dest_dir: Destination directory for sorted files
            criteria: Sorting criteria ('date', 'type', 'size', 'name')
            recursive: Whether to process subdirectories
        
        Returns:
            Dictionary containing sorting results and statistics
        """
        try:
            if criteria not in self.supported_criteria:
                raise ValueError(f"Unsupported sorting criteria. Supported: {self.supported_criteria}")

            # Create destination directory if it doesn't exist
            os.makedirs(dest_dir, exist_ok=True)

            # Collect all files
            files = []
            for root, _, filenames in os.walk(source_dir):
                if not recursive and root != source_dir:
                    continue
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    file_info = self.get_file_info(file_path)
                    if file_info:
                        files.append(file_info)

            # Sort files based on criteria
            if criteria == 'date':
                self._sort_by_date(files, dest_dir)
            elif criteria == 'type':
                self._sort_by_type(files, dest_dir)
            elif criteria == 'size':
                self._sort_by_size(files, dest_dir)
            elif criteria == 'name':
                self._sort_by_name(files, dest_dir)

            # Generate statistics
            stats = self._generate_statistics(files)
            
            return {
                'success': True,
                'message': f"Successfully sorted {len(files)} files by {criteria}",
                'statistics': stats
            }

        except Exception as e:
            logger.error(f"Error sorting files: {str(e)}")
            return {
                'success': False,
                'message': f"Error sorting files: {str(e)}",
                'statistics': None
            }

    def _sort_by_date(self, files: List[Dict], dest_dir: str):
        """Sort files by creation date."""
        for file_info in files:
            year_month = file_info['created'].strftime('%Y-%m')
            category_dir = os.path.join(dest_dir, year_month)
            self._move_file(file_info['path'], category_dir)

    def _sort_by_type(self, files: List[Dict], dest_dir: str):
        """Sort files by type/category."""
        for file_info in files:
            category_dir = os.path.join(dest_dir, file_info['category'])
            self._move_file(file_info['path'], category_dir)

    def _sort_by_size(self, files: List[Dict], dest_dir: str):
        """Sort files by size category."""
        size_categories = {
            'tiny': (0, 1024 * 100),  # 0 - 100KB
            'small': (1024 * 100, 1024 * 1024),  # 100KB - 1MB
            'medium': (1024 * 1024, 1024 * 1024 * 100),  # 1MB - 100MB
            'large': (1024 * 1024 * 100, 1024 * 1024 * 1024),  # 100MB - 1GB
            'huge': (1024 * 1024 * 1024, float('inf'))  # > 1GB
        }

        for file_info in files:
            for category, (min_size, max_size) in size_categories.items():
                if min_size <= file_info['size'] < max_size:
                    category_dir = os.path.join(dest_dir, category)
                    self._move_file(file_info['path'], category_dir)
                    break

    def _sort_by_name(self, files: List[Dict], dest_dir: str):
        """Sort files by first letter of name."""
        for file_info in files:
            first_letter = file_info['name'][0].upper()
            if not first_letter.isalpha():
                first_letter = '#'
            category_dir = os.path.join(dest_dir, first_letter)
            self._move_file(file_info['path'], category_dir)

    def _move_file(self, source_path: str, category_dir: str):
        """Move file to category directory, handling duplicates."""
        os.makedirs(category_dir, exist_ok=True)
        filename = os.path.basename(source_path)
        dest_path = os.path.join(category_dir, filename)

        # Handle duplicate filenames
        counter = 1
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(category_dir, f"{name}_{counter}{ext}")
            counter += 1

        shutil.move(source_path, dest_path)

    def _generate_statistics(self, files: List[Dict]) -> Dict[str, Any]:
        """Generate statistics about sorted files."""
        total_size = sum(f['size'] for f in files)
        categories = {}
        for file_info in files:
            category = file_info['category']
            if category not in categories:
                categories[category] = {'count': 0, 'total_size': 0}
            categories[category]['count'] += 1
            categories[category]['total_size'] += file_info['size']

        return {
            'total_files': len(files),
            'total_size': total_size,
            'categories': categories,
            'oldest_file': min(files, key=lambda x: x['created'])['created'] if files else None,
            'newest_file': max(files, key=lambda x: x['created'])['created'] if files else None
        }

    def extract_dates(self, file_content: str) -> List[datetime]:
        """Extract dates from the given file content using various formats."""
        # This is a placeholder for date extraction logic
        # You might want to use regex patterns or specialized libraries
        pass
