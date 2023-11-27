import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, dataSimItems: func.SqlRowList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get every row from database
    rows = list(map(lambda r: json.loads(r.to_json()), dataSimItems))

    # Initialise lists to track max, min and total values
    count = 0
    max_list = []
    min_list = []
    avg_list = []
    while count < 20:
        max_list.append([0, 0, 0, 0])
        min_list.append([3000, 3000, 3000, 3000])
        avg_list.append([0, 0, 0, 0])

        count = count + 1

    for r in rows:
        # mind max of each value
        if max_list[r.get("sensor_id")][0] < r.get("temperature"):
            max_list[r.get("sensor_id")][0] = r.get("temperature")
        if max_list[r.get("sensor_id")][1] < r.get("wind_speed"):
            max_list[r.get("sensor_id")][1] = r.get("wind_speed")
        if max_list[r.get("sensor_id")][2] < r.get("humidity"):
            max_list[r.get("sensor_id")][2] = r.get("humidity")
        if max_list[r.get("sensor_id")][3] < r.get("co2"):
            max_list[r.get("sensor_id")][3] = r.get("co2")

        # Find minimum of each vlaue
        if min_list[r.get("sensor_id")][0] > r.get("temperature"):
           min_list[r.get("sensor_id")][0] = r.get("temperature")
        if min_list[r.get("sensor_id")][1] > r.get("wind_speed"):
           min_list[r.get("sensor_id")][1] = r.get("wind_speed")
        if min_list[r.get("sensor_id")][2] > r.get("humidity"):
           min_list[r.get("sensor_id")][2] = r.get("humidity")
        if min_list[r.get("sensor_id")][3] > r.get("co2"):
           min_list[r.get("sensor_id")][3] = r.get("co2")

        # Keep running total of every value
        avg_list[r.get("sensor_id")][0] += r.get("temperature")
        avg_list[r.get("sensor_id")][1] += r.get("wind_speed")
        avg_list[r.get("sensor_id")][2] += r.get("humidity")
        avg_list[r.get("sensor_id")][3] += r.get("co2")

    # Find average from totals
    for i in avg_list:
        i[0] = i[0]/(len(rows)/20)
        i[1] = i[1]/(len(rows)/20)
        i[2] = i[2]/(len(rows)/20)
        i[3] = i[3]/(len(rows)/20)

    # Build output dictionary    
    output = []
    count = 0
    while count < 20:
        output.append({
            "sensor_id": count,
            "max_temperature": max_list[count][0],
            "max_wind_speed": max_list[count][1],
            "max_humidity": max_list[count][2],
            "max_co2": max_list[count][3],
            "min_temperature": min_list[count][0],
            "min_wind_speed": min_list[count][1],
            "min_humidity": min_list[count][2],
            "min_co2": min_list[count][3],
            "avg_temperature":  avg_list[count][0],
            "avg_wind_speed":  avg_list[count][1],
            "avg_humidity": avg_list[count][2],
            "avg_co2":  avg_list[count][3],
        })

        count = count + 1

    # Output as JSON
    return func.HttpResponse(
        json.dumps(output),
        status_code=200,
        mimetype="application/json"
    )

