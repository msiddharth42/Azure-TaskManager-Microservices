import azure.functions as func
import json

from services.task_service import TaskService

app = func.FunctionApp()

task_service = TaskService()


@app.route(route="tasks", methods=["POST"])
def create_task(req: func.HttpRequest) -> func.HttpResponse:

    try:

        body = req.get_json()

        title = body.get("title")

        if not title:
            return func.HttpResponse(
                json.dumps({"error": "title is required"}),
                status_code=400,
                mimetype="application/json"
            )

        task = task_service.create_task(title)

        return func.HttpResponse(
            json.dumps(task),
            status_code=201,
            mimetype="application/json"
        )

    except Exception as ex:

        return func.HttpResponse(
            json.dumps({"error": str(ex)}),
            status_code=500,
            mimetype="application/json"
        )