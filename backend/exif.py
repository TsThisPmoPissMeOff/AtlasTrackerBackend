import exifread
import io

def extract_exif(image_bytes):
    """Extract EXIF metadata from image."""
    try:
        f = io.BytesIO(image_bytes)
        tags = exifread.process_file(f, details=False)
        return {k: str(v) for k, v in tags.items()}
    except Exception as e:
        return f"EXIF extraction failed: {e}"
