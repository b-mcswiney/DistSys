import uuid
import json
import logging
import random
import azure.functions as func
from azure.functions.decorators.core import DataType


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="HttpTrigger1")
@app.route(route="data_sim")
@app.generic_output_binding(arg_name="dataSimItems", type="sql", CommandText="dbo.sim_data", ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING)
def data_sim(req: func.HttpRequest, dataSimItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data_lines_gen = req.params.get('iterations')

    req_body = req.get_json()

    if not data_lines_gen:
        try:
            req_body = req.get_json()
        except ValueError:
            data_lines_gen = 20
        else:
            data_lines_gen = req_body.get('iterations')

    count = 0
    data = []

    if not isinstance(data_lines_gen, int):
        data_lines_gen = 20

    while count < data_lines_gen:
        temperature = random.randint(8, 15)
        wind_speed = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)

        data.append([count, temperature, wind_speed, humidity, co2])
        
        count = count + 1

    dataSimItems.set(func.SqlRowList(map(genOutput, data)))

    return func.HttpResponse(
        "success",
        status_code=200
    )

"""
Generates output JSON structure
"""
def genOutput(x):
    return {"id": str(uuid.uuid4()),
            "sensor_id": x[0],
            "temperature": x[1],
            "wind_speed": x[2],
            "humidity": x[3],
            "co2": x[4]}