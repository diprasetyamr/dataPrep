import csv
import sys
import os
import datetime


class dataBase:
    id_measurement = 0
    wht = 0
    time = ""

    def __init__(self, var1, var2, var3):
        self.id_measurement = var1
        self.wht = var2
        self.time = var3


def createMeasurementDataList(measurmentdatafile, nodesorted):
    data_list = []
    found = 0
    with open(measurmentdatafile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for x in range(0, len(data_list)):
                if data_list[x][0] == row['node_id']:
                    found = 1
                    break
                else:
                    found = 0
            if found == 0:
                data_list.append([row['node_id'], [dataBase(
                    row['Id_Lectura'], row['W_hours_Total'], row['Fecha_Hora'])]])
            else:
                data_list[x][1].append(
                    dataBase(row['Id_Lectura'], row['W_hours_Total'], row['Fecha_Hora']))
    data_list.sort()
    filenames = nodesorted
    with open(filenames, 'w', newline='', encoding='utf-8') as csvfile:
        headers = ['node_id', 'Id_Lectura', 'W_hours_Total', 'Fecha_Hora']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for y in range(0, len(data_list)):
            for x in range(0, len(data_list[y][1])):
                writer.writerow({'node_id': data_list[y][0], 'Id_Lectura': data_list[y][1][x].id_measurement,
                                 'W_hours_Total': data_list[y][1][x].wht, 'Fecha_Hora': data_list[y][1][x].time})
    return data_list


def nodeList(sortedNodeFile, nodeTaken=0):
    node_list = []
    if nodeTaken != 0:
        measurement = 0
        nodesid = 0
        with open(sortedNodeFile, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['node_id']) != nodesid:
                    if len(node_list) < nodeTaken:
                        node_list.append([nodesid, measurement])
                    else:
                        if node_list[0][1] < measurement:
                            node_list[0][0] = nodesid
                            node_list[0][1] = measurement
                        node_list = sorted(node_list, key=lambda x: x[1])

                    nodesid = int(row['node_id'])
                    measurement = int(row['Id_Lectura'])

                else:
                    measurement = int(row['Id_Lectura'])
    else:
        previd = 0
        measurement = 0
        with open(sortedNodeFile, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if previd != int(row['node_id']):
                    node_list.append([row['node_id'], measurement])
                    previd = int(row['node_id'])

    return node_list


def generateData(data_list, node_list, datafolder):

    if not os.path.exists(datafolder):
        os.makedirs(datafolder)

    for x in range(0, len(data_list)):
        for y in range(0, len(node_list)):
            if int(data_list[x][0]) == node_list[y][0]:
                folderName = str(node_list[y][0])
                filenames = str(node_list[y][0]) + ".csv"

                if not os.path.exists(os.path.join(datafolder, folderName)):
                    os.makedirs(os.path.join(datafolder, folderName))

                prevHour = 0
                prevWatt = 0
                load = 0
                for z in range(0, len(data_list[x][1])):
                    timeStamp = datetime.datetime.strptime(
                        data_list[x][1][z].time, '%Y-%m-%d %H:%M:%S')
                    whichDays = (datetime.datetime.strptime(
                        data_list[x][1][z].time, '%Y-%m-%d %H:%M:%S')).isoweekday()
                    whichHour = (datetime.datetime.strptime(
                        data_list[x][1][z].time, '%Y-%m-%d %H:%M:%S')).hour

                    if z == 0:
                        prevWatt = float(data_list[x][1][z].wht)
                        prevHour = whichHour

                    if whichHour != prevHour:
                        load = float(data_list[x][1][z].wht) - prevWatt
                        prevWatt = float(data_list[x][1][z].wht)
                        prevHour = whichHour
                        if whichDays in range(1, 6):
                            folderName2 = "weekday"

                            if not os.path.exists(os.path.join(datafolder, folderName, folderName2)):
                                os.makedirs(os.path.join(
                                    datafolder, folderName, folderName2))

                            if os.path.exists(os.path.join(datafolder, folderName, folderName2, filenames)):
                                with open(os.path.join(datafolder, folderName, folderName2, filenames), 'a', newline='', encoding='utf-8') as csvfile:
                                    headers = ['Load', 'Hour',
                                               'Day', 'Timestamp']
                                    writer = csv.DictWriter(
                                        csvfile, fieldnames=headers)
                                    writer.writerow({'Load': load, 'Hour': whichHour,
                                                     'Day': whichDays, 'Timestamp': data_list[x][1][z].time})
                            else:
                                with open(os.path.join(datafolder, folderName, folderName2, filenames), 'a', newline='', encoding='utf-8') as csvfile:
                                    headers = ['Load', 'Hour',
                                               'Day', 'Timestamp']
                                    writer = csv.DictWriter(
                                        csvfile, fieldnames=headers)
                                    writer.writeheader()
                                    writer.writerow({'Load': load, 'Hour': whichHour,
                                                     'Day': whichDays, 'Timestamp': data_list[x][1][z].time})

                        else:
                            folderName2 = "weekend"

                            if not os.path.exists(os.path.join(datafolder, folderName, folderName2)):
                                os.makedirs(os.path.join(
                                    datafolder, folderName, folderName2))

                            if os.path.exists(os.path.join(datafolder, folderName, folderName2, filenames)):
                                with open(os.path.join(datafolder, folderName, folderName2, filenames), 'a', newline='', encoding='utf-8') as csvfile:
                                    headers = ['Load', 'Hour',
                                               'Day', 'Timestamp']
                                    writer = csv.DictWriter(
                                        csvfile, fieldnames=headers)
                                    writer.writerow({'Load': load, 'Hour': whichHour,
                                                     'Day': whichDays, 'Timestamp': data_list[x][1][z].time})
                            else:
                                with open(os.path.join(datafolder, folderName, folderName2, filenames), 'a', newline='', encoding='utf-8') as csvfile:
                                    headers = ['Load', 'Hour',
                                               'Day', 'Timestamp']
                                    writer = csv.DictWriter(
                                        csvfile, fieldnames=headers)
                                    writer.writeheader()
                                    writer.writerow({'Load': load, 'Hour': whichHour,
                                                     'Day': whichDays, 'Timestamp': data_list[x][1][z].time})
