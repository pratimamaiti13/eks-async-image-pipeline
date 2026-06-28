from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.s3 import s3_service
from app.services.job_service import job_service
from app.services.sqs import sqs_service

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    object_key = s3_service.upload_file(
        file.file,
        file.filename
    )

    job_id = job_service.create_job(object_key)

    sqs_service.send_message(
        job_id=job_id,
        object_key=object_key,
    )

    return {
        "message": "Upload successful",
        "job_id": job_id,
        "object_key": object_key
    }