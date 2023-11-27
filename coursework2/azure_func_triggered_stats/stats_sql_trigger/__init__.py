import logging
import json
import azure.functions as func


def main(changedData, allData: func.SqlRowList):
    # Get every row from database
    rows = list(map(lambda r: json.loads(r.to_json()), allData))

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

    # Output to logs
    count = 0
    output = ""
    while count < 20:
        output = output + "sensor:" + str(count)
        output = output + "\n max temperature: " + str(max_list[count][0])
        output = output + ", max wind speed: " + str(max_list[count][1])
        output = output + ", max humidity: " + str(max_list[count][2])
        output = output + ", max co2: " + str(max_list[count][3])
        output = output + "\n min temperature: " + str(min_list[count][0])
        output = output + ", min wind speed: " + str(min_list[count][1])
        output = output + ", min humidity: " + str(min_list[count][2])
        output = output + ", min co2: " + str(min_list[count][3])
        output = output + "\n avg temperature: " + str(avg_list[count][0])
        output = output + ", avg wind speed: " + str(avg_list[count][1])
        output = output + ", avg humidity: " + str(avg_list[count][2])
        output = output + ", avg co2: " + str(avg_list[count][3]) + "\n"
        count = count + 1
    logging.info(output)
