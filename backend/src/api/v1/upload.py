from fastapi import APIRouter, Depends, UploadFile, File
from src.core.dependencies import get_current_user
from src.models import User
from src.services import upload as upload_service

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a single image to Cloudinary.
    Returns the public URL and metadata.
    Use this for pre-uploading images before creating a post.
    """
    result = await upload_service.upload_image(file, folder="auragram/posts")
    return result
