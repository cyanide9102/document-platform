from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from document_platform.infrastructure.temporal.contracts import (
        DocumentWorkflowInput,
    )


@workflow.defn
class DocumentWorkflow:
    @workflow.run
    async def run(self, input: DocumentWorkflowInput):
        await workflow.execute_activity(
            "process_document",
            input,
            start_to_close_timeout=timedelta(minutes=5),
        )
