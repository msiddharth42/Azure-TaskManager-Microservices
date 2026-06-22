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

    def get_all_tasks(self):

        query = "SELECT * FROM c"

        tasks = list(
            self.db.container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )

        return tasks

    def get_task_by_id(self, task_id):

        try:

            task = self.db.container.read_item(
                item=task_id,
                partition_key=task_id
            )

            return task

        except Exception:

            return None

    def delete_task(self, task_id):

        try:

            self.db.container.delete_item(
                item=task_id,
                partition_key=task_id
            )

            return True

        except Exception:

            return False

    def update_task(self, task_id, title, status):

        task = self.get_task_by_id(task_id)

        if not task:
            return None

        task["title"] = title
        task["status"] = status

        updated = self.db.container.replace_item(
            item=task,
            body=task
        )

        return updated