import math
import re
import networkx as nx


def euclidean_distance_2d(x1, y1, x2, y2):
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)


def pseudo_eucledian(x1, y1, x2, y2):
    xd = x1 - x2
    yd = y1 - y2
    r12 = math.sqrt((xd*xd + yd*yd)/10.0)
    t12 = int(r12)
    if t12 < r12:
        distance = t12 - 1
    else:
        distance = t12

    return distance


def latitute_longitude(x1, y1):
    PI = 3.141592
    degrees_lat = int(x1)
    minutes_lat = x1 - degrees_lat
    latitude = PI * (degrees_lat + 5.0 * minutes_lat / 3.0) / 180.0
    degrees_long = int(y1)
    minutes_long = y1 - degrees_long
    longitude = PI * (degrees_long + 5.0 * minutes_long / 3.0) / 180.0
    return latitude, longitude


def geo_distance(x1, y1, x2, y2):

    RRR = 6378.388
    latitude1, longitude1 = latitute_longitude(x1, y1)
    latitude2, longitude2 = latitute_longitude(x2, y2)

    q1 = math.cos(longitude1-longitude2)
    q2 = math.cos(latitude1-latitude2)
    q3 = math.cos(latitude1 + latitude2)
    distance = int(RRR * math.acos(0.5*((1.0 + q1) * q2-(1.0-q1)*q3))+1.0)

    return distance


def file_to_list(filename):
    f = open(filename, "r")
    start_coordinates = False
    nodes_list = []
    for linha in f:
        content = re.findall("[^:]+", linha)

        if content[0] == "TYPE":
            graph_type = content[1]

        if content[0] == "DIMENSION":
            dimension = int(content[1])

        if content[0] == "EDGE_WEIGHT_TYPE":
            calculation_method = content[1]

        if start_coordinates:
            value = re.findall("\d+\.?\d*", linha)
            nodes_list.append(value)

        if start_coordinates and len(re.findall("\d+\.?\d*", linha)) == 0:
            start_coordinates = False

        if content[0] == "NODE_COORD_SECTION\n" or content[0] == "EDGE_WEIGHT_SECTION\n":
            start_coordinates = True

        if content[0] == "EOF\n":
            break
    nodes_list = nodes_list[:-1]
    return nodes_list, graph_type, calculation_method, dimension


def list_to_graph(graphlist, graphtype, calculation, dimension):

    if graphtype == " TSP\n":
        G = nx.Graph()

    flat_graph_list = [item for sublist in graphlist for item in sublist]

    for a in flat_graph_list:
        if a == "0":
            flat_graph_list.remove(a)

    print("length: ", len(flat_graph_list))
    print(flat_graph_list)
    if calculation == " EXPLICIT\n" and dimension == 21:
        counter = 0
        for i in range(1, dimension):
            for j in range(0, i):
                G.add_weighted_edges_from(
                    {(j, i, int(flat_graph_list[counter]))})
                counter += 1

    elif calculation == " EXPLICIT\n" and dimension != 21:
        counter = 0
        for i in range(len(graphlist)):
            for j in range(i+1, len(graphlist)+1):
                G.add_weighted_edges_from(
                    {(i, j, int(flat_graph_list[counter]))})
                counter += 1
    else:
        for i in range(len(graphlist)-1):
            for j in range(i+1, len(graphlist)):
                node1_num = int(graphlist[i][0]) - 1
                node2_num = int(graphlist[j][0]) - 1
                x1 = float(graphlist[i][1])
                y1 = float(graphlist[i][2])
                x2 = float(graphlist[j][1])
                y2 = float(graphlist[j][2])
                if calculation == " EUC_2D\n":
                    distance = euclidean_distance_2d(x1, y1, x2, y2)
                elif calculation == " GEO\n":
                    distance = geo_distance(x1, y1, x2, y2)
                elif calculation == " ATT\n":
                    distance = pseudo_eucledian(x1, y1, x2, y2)
                G.add_weighted_edges_from({(node1_num, node2_num, distance)})

    return G


def extract_graph(filename):
    graphlist, graphtype, calculation, dimension = file_to_list(filename)
    return list_to_graph(graphlist, graphtype, calculation, dimension)
