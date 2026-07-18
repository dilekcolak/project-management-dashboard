from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    uploaded_by: int
    original_filename: str
    content_type: str
    size: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int = Field(ge=0)