import os
import shutil
import tempfile
from fastapi import UploadFile, HTTPException
from imagekitio import ImageKit
from app.core.config import settings
import urllib.parse
import base64

imagekit = ImageKit(
    private_key=settings.IMAGEKIT_PRIVATE_KEY
)

def encode_text_for_overlay(text: str) -> str:
    if not text:
        return ""
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return urllib.parse.quote(base64_text)

def create_transformed_url(original_url: str, transformation_params: str, caption: str = None) -> str:
    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"

async def upload_file_to_imagekit(file: UploadFile) -> dict:
    tempfile_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            tempfile_path = tmp_file.name
            shutil.copyfileobj(file.file, tmp_file)

        upload_result = imagekit.files.upload(
            file=open(tempfile_path, "rb"),
            file_name=file.filename,
            use_unique_file_name=True,
            tags=["backend-upload"]
        )

        return {
            "url": upload_result.url,
            "file_name": upload_result.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tempfile_path and os.path.exists(tempfile_path):
            os.unlink(tempfile_path)
        file.file.close()
