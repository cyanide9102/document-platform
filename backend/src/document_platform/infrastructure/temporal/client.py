from temporalio.client import Client

from document_platform.config.settings import TemporalSettings


async def create_temporal_client(settings: TemporalSettings) -> Client:
    return await Client.connect(
        settings.host,
        namespace=settings.namespace,
    )
