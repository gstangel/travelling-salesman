from sys import maxsize
from os import path
import requests,json
import numpy as np
v = 4



# def tsp_solver(distance_matrix, starting_index):
#     vertex_dict = {}
#     for i in range(1, len(distance_matrix)):
#         vertex_dict[i + 1, ()] = distance_matrix[i][0]

#     min_path = maxsize
#     i = 0
#     while True:
#         i+= 1
#         current_cost = 0
#         k = starting_index
#         for i in range(len(vertex)):
#             current_cost += distance_matrix[k][vertex[i]]
#             k = vertex[i]
#         current_cost += distance_matrix[k][starting_index]
#         min_path = min(min_path, current_cost)

#         if not next_perm(vertex):
#             break

#     return min_path

# def get_minimum(starting_zip, zips):


# def get_zips_from_file():
#     num_points = 0
#     zips = []
    
#     #filename = input("What is the name of the file that contains the zip codes? (ex: zips.txt")
#     filename = "zips.txt"
#     # read the zips into an array
#     if path.exists(filename):
#         with open(filename, 'r') as zipfile:
#             lines = zipfile.readlines()
#             for line in lines:
#                 num_points += 1
#                 zips.append(line.rstrip())
#             return(num_points,zips)
#     else:
#         print("That file was not found")
#         exit()

#this functions uses googles distance matrix api to generate a distance matrix between all points
def generate_distance_matrix(num_points, zips):
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    api_key = "AIzaSyCMGwIHcaHwEYjeY_BV1vNJzyx9-eoWmJ4"
    distance_matrix = [[0 for col in range(num_points)] for row in range(num_points)] #generate the empty matrix
    
    for i in range(len(zips)):
        for j in range(len(zips)):
            source = zips[i]
            dest = zips[j]
            r = requests.get(url + 'origins=' + source +
                   '&destinations=' + dest +
                   '&key=' + api_key)
            data = r.json()
            print(data)
            destination_address = data['destination_addresses']
            distance_m = data['rows'][0]['elements'][0]['distance']['value']
            distance_matrix[i][j] = distance_m
            #print(distance_m)
            #zips[i][j] 
        
    return distance_matrix



if __name__ == "__main__":
        # these are def
    num_points, zips = get_zips_from_file()
    distance_matrix = generate_distance_matrix(num_points, zips)
    print(zips)
    print(np.array(distance_matrix))
    starting_index = 0
    #res = tsp_solver(distance_matrix,starting_index)
    print(res)