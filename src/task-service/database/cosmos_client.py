import os

from azure.cosmos import CosmosClient


class CosmosDB:

    def __init__(self):

        endpoint = os.getenv("COSMOS_ENDPOINT")
        key = os.getenv("COSMOS_KEY")

        client = CosmosClient(endpoint, key)

        database = client.get_database_client(
            os.getenv("COSMOS_DATABASE")
        )

        self.container = database.get_container_client(
            os.getenv("COSMOS_CONTAINER")
        )