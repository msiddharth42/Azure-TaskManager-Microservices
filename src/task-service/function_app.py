import azure.functions as func
import json

from services.task_service import TaskService

app = func.FunctionApp()

task_service = TaskService()

# add new task

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

# get all tasks

@app.route(route="tasks", methods=["GET"])
def get_tasks(req: func.HttpRequest):

    task_service = TaskService()

    tasks = task_service.get_all_tasks()

    return func.HttpResponse(
        json.dumps(tasks),
        mimetype="application/json",
        status_code=200
    )

# get task by id

@app.route(route="tasks/{id}", methods=["GET"])
def get_task(req: func.HttpRequest):

    task_id = req.route_params.get("id")

    task_service = TaskService()

    task = task_service.get_task_by_id(task_id)

    if not task:

        return func.HttpResponse(
            status_code=404
        )

    return func.HttpResponse(
        json.dumps(task),
        mimetype="application/json",
        status_code=200
    )

# update task

@app.route(route="tasks/{id}", methods=["PUT"])
def update_task(req: func.HttpRequest):

    task_id = req.route_params.get("id")

    body = req.get_json()

    title = body.get("title")
    status = body.get("status")

    service = TaskService()

    updated = service.update_task(
        task_id,
        title,
        status
    )

    if not updated:

        return func.HttpResponse(
            status_code=404
        )

    return func.HttpResponse(
        json.dumps(updated),
        mimetype="application/json",
        status_code=200
    )

# delete task

@app.route(route="tasks/{id}", methods=["DELETE"])
def delete_task(req: func.HttpRequest):

    task_id = req.route_params.get("id")

    service = TaskService()

    deleted = service.delete_task(task_id)

    if not deleted:

        return func.HttpResponse(
            status_code=404
        )

    return func.HttpResponse(
        status_code=204
    )