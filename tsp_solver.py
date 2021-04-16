from sys import maxsize
from os import path
import requests,json

v = 4


def travelling_salesman_function(graph, s):
    vertex = []
    for i in range(v):
        if i != s:
            vertex.append(i)

    min_path = maxsize
    while True:
        current_cost = 0
        k = s
        for i in range(len(vertex)):
            current_cost += graph[k][vertex[i]]
            k = vertex[i]
        current_cost += graph[k][s]
        min_path = min(min_path, current_cost)

        if not next_perm(vertex):
            break
    return min_path

def next_perm(l):
    n = len(l)
    i = n-2

    while i >= 0 and l[i] > l[i+1]:
        i -= 1
    
    if i == -1:
        return False

    j = i+1
    while j < n and l[j] > l[i]:
        j += 1

    j -= 1

    l[i], l[j] = l[j], l[i]
    left = i+1
    right = n-1

    while left < right:
        l[left], l[right] = l[right], l[left]
        left += 1
        right -= 1
    return True


def get_zips_from_file():
    num_points = 0
    zips = []
    
    filename = input("What is the name of the file that contains the zip codes? (ex: zips.txt")
    # read the zips into an array
    if path.exists(filename):
        with open(filename, 'r') as zipfile:
            lines = zipfile.readlines()
            for line in lines:
                num_points += 1
                zips.append(line)
            return(num_points,zips)
    else:
        print("That file was not found")
        exit()

#this functions uses googles distance matrix api to generate a distance matrix between all points
def generate_distance_matrix(num_points, zips):
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    api_key = "AIzaSyCMGwIHcaHwEYjeY_BV1vNJzyx9-eoWmJ4"
    distance_matrix = [[0 for col in range(num_points)] for row in range(num_points)] #generate the empty matrix
    
    for i in range(len(zips)):
        for j in range(i + 1,len(zips)):
            source = zips[i]
            dest = zips[j]
            r = requests.get(url + 'origins=' + source +
                   '&destinations=' + dest +
                   '&key=' + api_key)
            x = r.json()
            print(x)
        




if __name__ == "__main__":
        # these are def
    num_points, zips = get_zips_from_file()
    generate_distance_matrix(num_points, zips)
    # graph = [[0,10,15,20], [10,0,35,25], [15,35,0,30], [20,25,30,0]]
    # s = 0
    # res = travelling_salesman_function(graph,s)
    # print(res)