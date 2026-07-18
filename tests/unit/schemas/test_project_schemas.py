from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas.document import DocumentResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)


def test_project_create_with_valid_data() -> None:
    project = ProjectCreate(
        name="Project Management Dashboard",
        description="A REST API for project management.",
    )

    assert project.name == "Project Management Dashboard"
    assert project.description == "A REST API for project management."


def test_project_create_strips_name_whitespace() -> None:
    project = ProjectCreate(
        name="  Project Management Dashboard  ",
        description=None,
    )

    assert project.name == "Project Management Dashboard"


def test_project_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError, match="Project name cannot be empty"):
        ProjectCreate(
            name="   ",
            description="Description",
        )


def test_project_create_rejects_long_name() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(
            name="a" * 101,
            description="Description",
        )


def test_project_create_rejects_long_description() -> None:
    with pytest.raises(ValidationError):
        ProjectCreate(
            name="Project",
            description="a" * 2001,
        )


def test_project_create_converts_empty_description_to_none() -> None:
    project = ProjectCreate(
        name="Project",
        description="   ",
    )

    assert project.description is None


def test_project_update_accepts_only_name() -> None:
    update = ProjectUpdate(name="Updated Project")

    assert update.name == "Updated Project"
    assert update.description is None


def test_project_update_accepts_only_description() -> None:
    update = ProjectUpdate(description="Updated description")

    assert update.name is None
    assert update.description == "Updated description"


def test_project_update_accepts_empty_payload() -> None:
    update = ProjectUpdate()

    assert update.model_dump(exclude_unset=True) == {}


def test_project_update_excludes_unset_fields() -> None:
    update = ProjectUpdate(name="Updated Project")

    update_data = update.model_dump(exclude_unset=True)

    assert update_data == {"name": "Updated Project"}
    assert "description" not in update_data


def test_project_update_rejects_blank_name() -> None:
    with pytest.raises(ValidationError, match="Project name cannot be empty"):
        ProjectUpdate(name="   ")


def test_project_update_converts_empty_description_to_none() -> None:
    update = ProjectUpdate(description="   ")

    assert update.description is None


def test_project_response_has_empty_documents_by_default() -> None:
    response = ProjectResponse(
        id=1,
        owner_id=2,
        name="Project",
        description=None,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
    )

    assert response.documents == []


def test_project_response_includes_documents() -> None:
    document = DocumentResponse(
        id=10,
        project_id=1,
        uploaded_by=2,
        original_filename="requirements.pdf",
        content_type="application/pdf",
        size=1024,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
    )

    response = ProjectResponse(
        id=1,
        owner_id=2,
        name="Project",
        description="Description",
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
        documents=[document],
    )

    assert len(response.documents) == 1
    assert response.documents[0].id == 10
    assert response.documents[0].original_filename == "requirements.pdf"


def test_project_response_can_be_created_from_attributes() -> None:
    created_at = datetime(2026, 7, 18, tzinfo=UTC)

    database_project = SimpleNamespace(
        id=1,
        owner_id=2,
        name="Project",
        description="Description",
        created_at=created_at,
        updated_at=None,
        documents=[],
    )

    response = ProjectResponse.model_validate(database_project)

    assert response.id == 1
    assert response.owner_id == 2
    assert response.name == "Project"
    assert response.documents == []


def test_project_list_response_with_projects() -> None:
    project = ProjectResponse(
        id=1,
        owner_id=2,
        name="Project",
        description=None,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
        updated_at=None,
    )

    response = ProjectListResponse(
        projects=[project],
        total=1,
    )

    assert len(response.projects) == 1
    assert response.total == 1
    assert response.projects[0].name == "Project"


def test_project_list_response_accepts_empty_list() -> None:
    response = ProjectListResponse(
        projects=[],
        total=0,
    )

    assert response.projects == []
    assert response.total == 0


def test_project_list_response_rejects_negative_total() -> None:
    with pytest.raises(ValidationError):
        ProjectListResponse(
            projects=[],
            total=-1,
        )