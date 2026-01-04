import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import asyncio
from typing import List, Tuple, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image conversion and compression."""
    
    SUPPORTED_INPUT_FORMATS = {
        '.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif'
    }
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    async def process_files(
        self,
        file_paths: List[str],
        output_format: str,
        quality: Optional[int] = None,
        dimensions: Optional[Tuple[int, Optional[int]]] = None,
        status_callback: Optional[Callable] = None
    ) -> str:
        """Process all files and return path to output ZIP."""
        
        # Extract all images from ZIPs and direct uploads
        all_images = []
        
        for file_path in file_paths:
            if await self._update_status(status_callback, f"🔍 Processing {Path(file_path).name}..."):
                pass
            
            if file_path.lower().endswith('.zip'):
                # Extract ZIP and get images
                images = await self._extract_zip(file_path)
                all_images.extend(images)
            else:
                # Direct image file
                ext = Path(file_path).suffix.lower()
                if ext in self.SUPPORTED_INPUT_FORMATS:
                    all_images.append({
                        'path': file_path,
                        'relative_path': Path(file_path).name,
                        'original_name': Path(file_path).name
                    })
        
        if not all_images:
            raise ValueError("No valid images found in uploaded files")
        
        # Convert images
        converted_dir = tempfile.mkdtemp()
        total = len(all_images)
        
        for idx, img_info in enumerate(all_images, 1):
            if await self._update_status(
                status_callback,
                f"🔄 Converting {idx}/{total}: {img_info['original_name']}"
            ):
                pass
            
            try:
                output_path = await self._convert_image(
                    img_info['path'],
                    img_info['relative_path'],
                    converted_dir,
                    output_format,
                    quality,
                    dimensions
                )
            except Exception as e:
                logger.error(f"Error converting {img_info['original_name']}: {e}")
                continue
        
        # Create output ZIP
        if await self._update_status(status_callback, "📦 Creating ZIP file..."):
            pass
        
        output_zip = os.path.join(self.temp_dir, 'converted_images.zip')
        await self._create_zip(converted_dir, output_zip)
        
        # Cleanup
        shutil.rmtree(converted_dir, ignore_errors=True)
        
        if await self._update_status(status_callback, "✅ Conversion complete!"):
            pass
        
        return output_zip
    
    async def _extract_zip(self, zip_path: str) -> List[dict]:
        """Extract images from ZIP file."""
        images = []
        extract_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find all images
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in self.SUPPORTED_INPUT_FORMATS:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, extract_dir)
                    
                    images.append({
                        'path': full_path,
                        'relative_path': relative_path,
                        'original_name': file
                    })
        
        return images
    
    async def _convert_image(
        self,
        input_path: str,
        relative_path: str,
        output_base_dir: str,
        output_format: str,
        quality: Optional[int],
        dimensions: Optional[Tuple[int, Optional[int]]]
    ) -> str:
        """Convert a single image."""
        
        # Open image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if saving as JPEG
        if output_format in ['JPEG', 'JPG'] and img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if dimensions specified
        if dimensions:
            width, height = dimensions
            if height is None:
                # Maintain aspect ratio
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Prepare output path (maintain directory structure)
        path_parts = Path(relative_path).parts
        if len(path_parts) > 1:
            output_dir = os.path.join(output_base_dir, *path_parts[:-1])
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = output_base_dir
        
        # Change extension to output format
        output_filename = Path(path_parts[-1]).stem + f'.{output_format.lower()}'
        output_path = os.path.join(output_dir, output_filename)
        
        # Save with quality
        save_kwargs = {}
        if output_format in ['JPEG', 'JPG']:
            save_kwargs['quality'] = quality if quality else 95
            save_kwargs['optimize'] = True
        elif output_format == 'PNG':
            if quality and quality < 100:
                # PNG compression level (0-9)
                save_kwargs['compress_level'] = int((100 - quality) / 100 * 9)
            else:
                save_kwargs['compress_level'] = 6
        elif output_format == 'WEBP':
            save_kwargs['quality'] = quality if quality else 90
            save_kwargs['method'] = 6
        
        img.save(output_path, format=output_format, **save_kwargs)
        return output_path
    
    async def _create_zip(self, source_dir: str, output_path: str):
        """Create ZIP file from directory."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    async def _update_status(self, callback: Optional[Callable], message: str) -> bool:
        """Update status via callback."""
        if callback:
            try:
                await callback(message)
                await asyncio.sleep(0.1)  # Small delay for UI update
                return True
            except Exception as e:
                logger.warning(f"Status update failed: {e}")
        return False
    
    def cleanup(self):
        """Cleanup temporary files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
