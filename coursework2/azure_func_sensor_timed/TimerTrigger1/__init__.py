import datetime
import logging
import uuid
import random
import azure.functions as func


def main(mytimer: func.TimerRequest, dataSimItems: func.Out[func.SqlRow]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat
    
    count = 0
    data = []

    while count < 20:
        temperature = random.randint(8, 15)
        wind_speed = random.randint(15, 25)
        humidity = random.randint(40, 70)
        co2 = random.randint(500, 1500)

        data.append([count, temperature, wind_speed, humidity, co2])
        
        count = count + 1

    dataSimItems.set(func.SqlRowList(map(genOutput, data)))


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

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
