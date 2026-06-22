import uuid
from datetime import datetime

from database.cosmos_client import CosmosDB


class TaskService:

    def __init__(self):
        self.db = CosmosDB()

    def create_task(self, title):

        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat()
        }

        self.db.container.create_item(task)

        return task