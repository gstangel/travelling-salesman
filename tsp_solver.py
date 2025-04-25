from os import path
import requests
from itertools import combinations

# bottom-up dynamic programming approach
def calculate_tsp(adjacency_matrix) -> tuple:
    # map  each subset of the nodes to the cost to reach that subset
    SUBSETS = {}

    # Set transition cost from initial state
    for k in range(1, len(adjacency_matrix)):
        SUBSETS[(1 << k, k)] = (adjacency_matrix[0][k], 0) # using the bits of an integer to encode the verticies' index by bitshifting
        # for example, we could encode the set of indicies {0,3,4} into the binary where 2^0 + 2^3 + 2^4 = 11001

    # Bottom-up dynamic programming approach 
    for subset_size in range(2, len(adjacency_matrix)):
        for subset in combinations(range(1, len(adjacency_matrix)), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k) # bitshifting
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((SUBSETS[(prev, m)][0] + adjacency_matrix[m][k], m))
                SUBSETS[(bits, k)] = min(res)
    bits = (2**len(adjacency_matrix) - 1) - 1

    # Calculate lowest cost
    res = []
    for k in range(1, len(adjacency_matrix)):
        res.append((SUBSETS[(bits, k)][0] + adjacency_matrix[k][0], k))
    cost, parent = min(res)

    # backtracking step
    path = []
    for i in range(len(adjacency_matrix) - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = SUBSETS[(bits, parent)]
        bits = new_bits

    path.append(0) # add starting zip
    path.insert(0,0) # start and end at the same place
    cost += adjacency_matrix[path[-1]][0] # return to the start of the tour
    return cost, list(reversed(path)) # reverse the path since we used a bottom up approach

#this function returns the zips read from the file in a python list
def get_zips_from_file() -> list:
    print("Loading the zip codes...")
    num_points = 0 # counter for the number of zips in the file
    zips = [] # empty list
    
    filename = input("What is the name of the file that contains the zip codes? (ex: zips.txt)  ") #prompt user for filename

    # read the zips into an array
    if path.exists(filename): #if the file exists
        with open(filename, 'r') as zipfile: #open it
            lines = zipfile.readlines() # read the lines
            for line in lines: # iterate through the lines
                num_points += 1 # increment the number of points with every read
                zips.append(line.rstrip()) # add the zip code to ouur list
            return(num_points,zips) # return the zip codes
    else:
        print("That file was not found") # throw an error if there is no file with that name
        exit()

#this functions uses googles distance matrix api to generate a distance matrix between all points
def generate_distance_matrix(num_points, zips) -> list:
    print("Gathering distance data from Google's distance matrix API...")
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?' # the url that you send request to
    api_key = "" # this is how google knows we are authenticated to use this API

    #generate the empty distance matrix, if the number of zips is 7, this line will produce a 7x7 2d array of 0's
    #distance_matrix = [[DistanceMatrixPoint() for col in range(num_points)] for row in range(num_points)] 
    distance_matrix = [[0 for col in range(num_points)] for row in range(num_points)] 
    for i in range(len(zips)): #iterate through the zip codes, making number_of_zips^2 api calls
        print('%.2f'%(i/len(distance_matrix) * 100 ), "percent complete") # print percentage complete formatted to two decimal places
        for j in range(len(zips)):
            source = zips[i]
            dest = zips[j]

            r = requests.get(url + 'origins=' + source +  #make the API request
                   '&destinations=' + dest +
                   '&key=' + api_key)

            data = r.json() #convert the response to a json 
            distance_km = int(data['rows'][0]['elements'][0]['distance']['value'] / 1000) #extract the distance in meters from the api response, convert to KM by / 1000
            distance_matrix[i][j] = distance_km #put the distance in meters from the api response into our array

    return distance_matrix # return it back to our main function

# this function generates a url with the google maps link to the tour
def generate_maps_url(tour, zips) -> str:
    url = "https://www.google.com/maps/dir/"
    for index in tour:
        url += str(zips[index]) + "/"
    return url
    


if __name__ == "__main__":
        # these are def
    num_points, zips = get_zips_from_file() # read the zips in from the file
    adjacency_matrix = generate_distance_matrix(num_points, zips) #generate the populated adjacency matrix

    tour_cost, tour = calculate_tsp(adjacency_matrix) # solve tsp using our adjacency matrix and DP
    print("The total cost of the tour was : " + str(tour_cost/1.609) + " miles")
    
    url = generate_maps_url(tour, zips)
    print(url)
