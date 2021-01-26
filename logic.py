# Read all input from a file and return array of all numberedPlates arrays (ie [ [1,3,5,4,2],[1,2,3] ])
#
# For each numberedPlates array do the following:
#  1. create sorted numberedPlatesMap holding sorted PlateNodes (index in numberedPlates where it's located,
#     previous PlateNode, next PlateNode, and the number itself)
#
#  2. until the numberedPlates array is of len 0, continue cutting it from both sides
#
#  3. cutting the numberedPlates will happen through accessing the first and last PlateNodes in numberedPlatesMap
#     to get the indexes of lowest/highest numbers left in the numberedPlates
#       - when cut happens, for all nums that has been cut away, remove their corresponding PlateNodes in the numberedPlatesMap
#

import time

# Creating the numberedPlatesMap (1 function and 1 Class):
class PlateNode():

    def __init__(self, holdingNumber, numberIndexInNumberedPlatesArray, nextPlateNode=None, previousPlateNode=None):
        self.holdingNumber = holdingNumber
        self.numberIndexInNumberedPlatesArray = numberIndexInNumberedPlatesArray

        self.nextPlateNode = self.previousPlateNode = None

def createNumberedPlatesMap(numberedPlates):
    
    numberedPlatesMap = []

    # Go through all plates and create for them PlateNodes in numberedPlatesMap
    for plate_index,plate_num in enumerate(numberedPlates):

        insertion_index = 0
        newPlateNode = PlateNode(plate_num,plate_index)

        if len(numberedPlatesMap) > 0:
            current = numberedPlatesMap[0]

            while current != None:

                if current.holdingNumber > plate_num: # Found first higher number, insert it here
                    newPlateNode.previousPlateNode = current.previousPlateNode
                    if current.previousPlateNode:
                        current.previousPlateNode.nextPlateNode = newPlateNode
                    current.previousPlateNode = newPlateNode
                    newPlateNode.nextPlateNode = current
                    break

                current = current.nextPlateNode

                if current == None: # Went all the way to the end of the list
                    newPlateNode.previousPlateNode = numberedPlatesMap[-1]
                    numberedPlatesMap[-1].nextPlateNode = newPlateNode

                insertion_index += 1
        
        numberedPlatesMap.insert( insertion_index, newPlateNode )

    return numberedPlatesMap


# Reading the input (2 functions):
def createArrayFromOneNumberedPlatesGame(num_of_plates_string_line, plates_string_line):

    # First read the num_of_plates:
    num_of_plates = ""
    for char in num_of_plates_string_line:
        if char != " ":
            num_of_plates += char
        else:
            break
    
    num_of_plates = int(num_of_plates)


    # Now read all the plates:
    plates_array = []
    char_index = 0
    for _ in range(0,num_of_plates):
        this_plate = ""
        while True:
            if plates_string_line[char_index] != " " and plates_string_line[char_index] != "\n":
                this_plate += plates_string_line[char_index]
                char_index += 1
                if char_index >= len(plates_string_line): # End of the line without the "\n"
                    break
            else:
                char_index += 1
                break
        plates_array.append(int(this_plate))
    
    return plates_array

def readFileIntoArrayOfArrays(raw_file):
    # arrayOfNumberedPlates will have all numberedPlates arrays and will be returned
    arrayOfNumberedPlates = []

    # How many arrays will I generate:
    num_of_games = raw_file.readline()

    # Read two lines for each numberedPlates game and create array from it to append
    for _ in range(0,int(num_of_games)):
        array_for_this_one_game = createArrayFromOneNumberedPlatesGame(raw_file.readline(), raw_file.readline())
        arrayOfNumberedPlates.append(array_for_this_one_game)

    return arrayOfNumberedPlates


# Main algorithms for each game to play (2 functions):
def removeFromNumberedPlatesMap(plate_nodes_numbers_to_remove,numbered_plates_map):
    current = numbered_plates_map[0]
    index_of_plate_node = 0

    while current != None:
        # if the current PlateNode is holding the number from the plate_nodes_numbers_to_remove array, pop it out
        if current.holdingNumber in plate_nodes_numbers_to_remove:
            if current.previousPlateNode:
                current.previousPlateNode.nextPlateNode = current.nextPlateNode
            if current.nextPlateNode:
                current.nextPlateNode.previousPlateNode = current.previousPlateNode
            numbered_plates_map.pop(index_of_plate_node)
            index_of_plate_node -= 1

        current = current.nextPlateNode
        index_of_plate_node += 1
    
    return numbered_plates_map

def playGame(numbered_plates, numbered_plates_map):
    my_turn = True # Trying the game if I start the game
    #numbered_plates_current = numbered_plates

    while len(numbered_plates_map) >= 1:

        if my_turn: # I'm taking away the plate with highest num
            index_of_highest = numbered_plates_map[-1].numberIndexInNumberedPlatesArray # FIX: The index is constant - not being updated when we pop out some nodes

            # Removal of the plates which I took away as well:
            plate_nodes_numbers_to_remove = numbered_plates[index_of_highest:]
            numbered_plates_map = removeFromNumberedPlatesMap(plate_nodes_numbers_to_remove,numbered_plates_map)

            #numbered_plates_current = numbered_plates[:index_of_highest]

        else: # He is taking away the plate with lowest num
            index_of_lowest = numbered_plates_map[0].numberIndexInNumberedPlatesArray # FIX: The index is constant - not being updated when we pop out some nodes

            # Removal of the plates which he took away as well:
            plate_nodes_numbers_to_remove = numbered_plates[:index_of_lowest+1]
            numbered_plates_map = removeFromNumberedPlatesMap(plate_nodes_numbers_to_remove,numbered_plates_map)

            #numbered_plates_current = numbered_plates[index_of_lowest+1:]

        if my_turn:
            my_turn = False
        else:
            my_turn = True

    if my_turn:
        return("DRUHY")
    else:
        return("PRVNI")


# Going through all numberedPlates arrays and receiveing their input (1 function):
def playAllGames(raw_file):
    array_of_all_numberedPlates_games = readFileIntoArrayOfArrays(raw_file)
    resulting_decisions_for_each_game = []

    for numberedPlates in array_of_all_numberedPlates_games:
        print(numberedPlates)
        numbered_plates_map = createNumberedPlatesMap(numberedPlates)
        result_for_this_game = playGame(numberedPlates, numbered_plates_map)
        resulting_decisions_for_each_game.append(result_for_this_game)

    return resulting_decisions_for_each_game

# UI function (1 function):
def main(name_of_input_file, name_of_output_file="RESULTS"):
    raw_file = open(name_of_input_file, "r")
    array_of_results = playAllGames(raw_file)
    raw_file.close()
    
    results_file = open(name_of_output_file,"w")
    for result in array_of_results:
        results_file.writelines(result+"\n")

    results_file.close()
    return True



start_time = time.time()

main("input.txt","RESULTS_test_input.txt")

print("--- %s seconds ---" % (time.time() - start_time))



