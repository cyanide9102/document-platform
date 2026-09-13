import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from document_platform.config.settings import settings
from document_platform.infrastructure.temporal.activities import (
    DocumentActivities,
)
from document_platform.infrastructure.temporal.workflows import DocumentWorkflow


async def run_worker(
    temporal_client: Client,
    activities: DocumentActivities,
):
    worker = Worker(
        temporal_client,
        task_queue=settings.temporal.task_queue,
        workflows=[DocumentWorkflow],
        activities=[activities.process_document],
    )

    await worker.run()


async def main():
    temporal_client = await Client.connect(
        settings.temporal.host,
        namespace=settings.temporal.namespace,
    )

    activities = DocumentActivities()

    await run_worker(temporal_client=temporal_client, activities=activities)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker stopped.")
