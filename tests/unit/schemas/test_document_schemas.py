from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas.document import DocumentListResponse, DocumentResponse


def test_document_response_with_valid_data() -> None:
    created_at = datetime(2026, 7, 18, 10, 30, tzinfo=UTC)

    document = DocumentResponse(
        id=1,
        project_id=2,
        uploaded_by=3,
        original_filename="requirements.pdf",
        content_type="application/pdf",
        size=2048,
        created_at=created_at,
        updated_at=None,
    )

    assert document.id == 1
    assert document.project_id == 2
    assert document.uploaded_by == 3
    assert document.original_filename == "requirements.pdf"
    assert document.content_type == "application/pdf"
    assert document.size == 2048
    assert document.created_at == created_at
    assert document.updated_at is None


def test_document_response_rejects_negative_size() -> None:
    with pytest.raises(ValidationError):
        DocumentResponse(
            id=1,
            project_id=2,
            uploaded_by=3,
            original_filename="requirements.pdf",
            content_type="application/pdf",
            size=-1,
            created_at=datetime(2026, 7, 18, tzinfo=UTC),
            updated_at=None,
        )


def test_document_response_can_be_created_from_attributes() -> None:
    created_at = datetime(2026, 7, 18, tzinfo=UTC)

    database_document = SimpleNamespace(
        id=1,
        project_id=2,
        uploaded_by=3,
        original_filename="requirements.pdf",
        content_type="application/pdf",
        size=2048,
        created_at=created_at,
        updated_at=None,
    )

    response = DocumentResponse.model_validate(database_document)

    assert response.id == 1
    assert response.original_filename == "requirements.pdf"
    assert response.size == 2048


def test_document_response_does_not_expose_s3_key() -> None:
    document = DocumentResponse(
        id=1,
        project_id=2,
        uploaded_by=3,
        original_filename="requirements.pdf",
        content_type="application/pdf",
        size=2048,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
    )

    response_data = document.model_dump()

    assert "s3_key" not in response_data


def test_document_list_response_with_documents() -> None:
    document = DocumentResponse(
        id=1,
        project_id=2,
        uploaded_by=3,
        original_filename="requirements.pdf",
        content_type="application/pdf",
        size=2048,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
    )

    response = DocumentListResponse(
        documents=[document],
        total=1,
    )

    assert len(response.documents) == 1
    assert response.total == 1
    assert response.documents[0].original_filename == "requirements.pdf"


def test_document_list_response_accepts_empty_list() -> None:
    response = DocumentListResponse(
        documents=[],
        total=0,
    )

    assert response.documents == []
    assert response.total == 0


def test_document_list_response_rejects_negative_total() -> None:
    with pytest.raises(ValidationError):
        DocumentListResponse(
            documents=[],
            total=-1,
        )