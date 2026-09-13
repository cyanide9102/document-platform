from uuid import UUID

from temporalio.client import Client

from document_platform.application.processing.ports import DocumentWorkflowStarter
from document_platform.config.settings import TemporalSettings
from document_platform.infrastructure.temporal.contracts import DocumentWorkflowInput
from document_platform.infrastructure.temporal.workflows import DocumentWorkflow


class TemporalDocumentWorkflowStarter(DocumentWorkflowStarter):
    def __init__(self, client: Client, settings: TemporalSettings):
        self._client = client
        self._settings = settings

    async def start(self, document_id: UUID):
        await self._client.start_workflow(
            DocumentWorkflow.run,
            DocumentWorkflowInput(document_id=document_id),
            id=f"document-{document_id}",
            task_queue=self._settings.task_queue,
        )
