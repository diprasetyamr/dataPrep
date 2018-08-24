from dataPrepSTLF import nodeList, createMeasurementDataList, generateData

data_list = []
node_list = []
measurmentdatafile = 'load_forecast_dashboard_measure.csv'
nodedatafile = 'load_forecast_dashboard_node.csv'
nodesorted = 'node_sorted.csv'
datafolder = 'data'

data_list = createMeasurementDataList(measurmentdatafile,nodesorted)

node_list = nodeList(nodesorted, 3)

generateData(data_list,node_list,datafolder)
