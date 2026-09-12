from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from document_platform.application.schemas.use_cases import (
    CreateXmlSchemaUseCase,
    DeleteXmlSchemaUseCase,
    GetXmlSchemaUseCase,
    ListXmlSchemasUseCase,
)
from document_platform.presentation.api.dependencies import (
    get_create_xml_schema_use_case,
    get_delete_xml_schema_use_case,
    get_list_xml_schemas_use_case,
    get_xml_schema_use_case,
)
from document_platform.presentation.api.v1.dtos import SchemaResponse

router = APIRouter(
    prefix="/schemas",
    tags=["schemas"],
)


@router.post(
    "",
    response_model=SchemaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_schema(
    file: UploadFile = File(...),
    name: str = Form(...),
    use_case: CreateXmlSchemaUseCase = Depends(get_create_xml_schema_use_case),
) -> SchemaResponse:
    schema = await use_case.execute(name=name, content=file.file)

    return SchemaResponse(
        id=schema.id,
        name=schema.name,
        size=schema.size,
        created_at=schema.created_at,
    )


@router.delete(
    "/{schema_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_schema(
    schema_id: UUID,
    use_case: DeleteXmlSchemaUseCase = Depends(get_delete_xml_schema_use_case),
):
    await use_case.execute(schema_id)


@router.get(
    "",
    response_model=list[SchemaResponse],
)
async def get_schemas(
    use_case: ListXmlSchemasUseCase = Depends(get_list_xml_schemas_use_case),
) -> list[SchemaResponse]:
    schemas = await use_case.execute()

    return [
        SchemaResponse(
            id=schema.id,
            name=schema.name,
            size=schema.size,
            created_at=schema.created_at,
        )
        for schema in schemas
    ]


@router.get(
    "/{schema_id}",
    response_model=SchemaResponse,
)
async def get_schema(
    schema_id: UUID,
    use_case: GetXmlSchemaUseCase = Depends(get_xml_schema_use_case),
) -> SchemaResponse:
    schema = await use_case.execute(schema_id)

    return SchemaResponse(
        id=schema.id,
        name=schema.name,
        size=schema.size,
        created_at=schema.created_at,
    )
