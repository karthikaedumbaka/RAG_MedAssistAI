from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from modules.load_vectorstore import load_vectorstore
from logger import logger

router = APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"📂 Received {len(files)} uploaded file(s).")

        # Call load_vectorstore directly (synchronous)
        load_vectorstore(files)

        logger.info("✅ Documents successfully added to VectorStore")
        return {"message": "Files processed and VectorStore updated"}

    except Exception as e:
        logger.exception("❌ Error during PDF upload.")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
