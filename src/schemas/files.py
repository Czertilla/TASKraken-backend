from datetime import datetime
from typing import Annotated, List, Optional, Union
from uuid import UUID
from fastapi import Body, Depends, File, Form, Query, UploadFile
from pydantic import BaseModel, Field

async def upload_file(file: UploadFile = File(...)) -> UploadFile:
    return file

async def upload_folder(files: list[UploadFile] = []) -> list[UploadFile]:
    return [await upload_file(file) for file in files]

class SFolderUpload(BaseModel):
    folder: list[Annotated[UploadFile, File(...)]] = Depends(upload_folder)