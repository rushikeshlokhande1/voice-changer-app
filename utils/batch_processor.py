"""
Batch processing module for handling multiple audio files.
Supports batch voice conversion and ZIP file creation.
"""

import os
import tempfile
import zipfile
from typing import List, Tuple, Callable, Optional
from pathlib import Path
import shutil


class BatchProcessor:
    """Handles batch processing of multiple audio files."""
    
    def __init__(self):
        """Initialize batch processor."""
        self.temp_dir = None
        self.processed_files = []
    
    def create_temp_directory(self) -> str:
        """
        Create a temporary directory for batch processing.
        
        Returns:
            Path to temporary directory
        """
        self.temp_dir = tempfile.mkdtemp(prefix="voice_batch_")
        return self.temp_dir
    
    def process_batch(
        self,
        audio_files: List[str],
        process_function: Callable,
        **kwargs
    ) -> Tuple[List[str], List[str]]:
        """
        Process multiple audio files with the same effect.
        
        Args:
            audio_files: List of audio file paths
            process_function: Function to apply to each file
            **kwargs: Additional arguments for process_function
        
        Returns:
            Tuple of (successful_files, error_messages)
        """
        if not self.temp_dir:
            self.create_temp_directory()
        
        successful = []
        errors = []
        
        for i, audio_file in enumerate(audio_files):
            try:
                # Get original filename
                original_name = Path(audio_file).stem
                output_path = os.path.join(
                    self.temp_dir,
                    f"{original_name}_processed.wav"
                )
                
                # Process file
                result = process_function(audio_file, output_path, **kwargs)
                
                if result:
                    successful.append(output_path)
                    self.processed_files.append(output_path)
                else:
                    errors.append(f"File {i+1}: Processing failed")
                    
            except Exception as e:
                errors.append(f"File {i+1} ({Path(audio_file).name}): {str(e)}")
        
        return successful, errors
    
    def create_zip(self, output_path: str, files: List[str]) -> str:
        """
        Create a ZIP file containing all processed files.
        
        Args:
            output_path: Path for the output ZIP file
            files: List of files to include
        
        Returns:
            Path to created ZIP file
        """
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    if os.path.exists(file_path):
                        # Add file with just the filename (no path)
                        arcname = os.path.basename(file_path)
                        zipf.write(file_path, arcname=arcname)
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error creating ZIP file: {str(e)}")
    
    def cleanup(self):
        """Clean up temporary directory and files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
                self.processed_files = []
            except Exception as e:
                print(f"Warning: Could not clean up temp directory: {str(e)}")
    
    def get_progress_message(self, current: int, total: int, filename: str = "") -> str:
        """
        Generate progress message.
        
        Args:
            current: Current file number
            total: Total number of files
            filename: Optional filename being processed
        
        Returns:
            Progress message string
        """
        percentage = (current / total) * 100
        file_info = f" - {filename}" if filename else ""
        return f"Processing {current}/{total} ({percentage:.1f}%){file_info}"


def validate_audio_files(files: List, max_files: int = 30) -> Tuple[bool, str]:
    """
    Validate uploaded audio files.
    
    Args:
        files: List of uploaded files
        max_files: Maximum number of files allowed
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not files:
        return False, "No files uploaded"
    
    if len(files) > max_files:
        return False, f"Too many files! Maximum {max_files} files allowed, got {len(files)}"
    
    # Check file types
    valid_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}
    for file in files:
        if file is None:
            continue
        ext = Path(file.name if hasattr(file, 'name') else str(file)).suffix.lower()
        if ext not in valid_extensions:
            return False, f"Invalid file type: {ext}. Supported: WAV, MP3, M4A, FLAC, OGG"
    
    return True, "Files validated successfully"


def get_batch_summary(successful: int, failed: int, total: int) -> str:
    """
    Generate batch processing summary.
    
    Args:
        successful: Number of successful files
        failed: Number of failed files
        total: Total number of files
    
    Returns:
        Summary message
    """
    if failed == 0:
        return f"✅ All {total} files processed successfully!"
    elif successful == 0:
        return f"❌ All {total} files failed to process"
    else:
        return f"⚠️ Processed {successful}/{total} files successfully ({failed} failed)"
