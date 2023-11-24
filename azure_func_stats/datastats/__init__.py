import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, dataSimItems: func.SqlRowList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rows = list(map(lambda r: json.loads(r.to_json()), dataSimItems))

    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json"
    )
