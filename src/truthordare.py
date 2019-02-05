from random import *

#user_input = ""
#num_players = ""
current_player = 0
player_number = current_player
extreme_point_dict = {}
last_was_truth = False


def make_list(fileName):
    sourceFile = open(fileName)
    
    #Taken from http://stackoverflow.com/questions/4842057/python-easiest-way-to-ignore-blank-lines-when-reading-a-file
    lines = (line.rstrip() for line in sourceFile) 
    itemList = list(line for line in lines if line)
    
    shuffle(itemList)
    return itemList

def getCategoryFromDistribution(probabilityDistribution):
    randomProbability = uniform(0, 1)
    for i in range(len(probabilityDistribution)):
        if randomProbability <= probabilityDistribution[i]:
            return i
#Process method using only player number
'''
def process(line, num_players):
    player_number = randint(1, num_players)
    player_reference = "Player " + str(player_number)
    new_line = line.replace("someone", player_reference)
    return new_line
'''
#Process method using name
def process(line, player_names):
    global player_number
    player_number = current_player
    while(player_number == current_player):
        player_number = randint(1, len(player_names)) - 1
    player_reference = str(player_names[player_number])
    new_line = line.replace("someone", player_reference)
    return new_line 

#def process(line):
    #return line

def getNumPlayersAggressively(user_input):
    num_players = ""
    print('"', user_input, '"', " players huh?")
    
    while not isinstance(num_players, int) or num_players < 1:
        try: 
            user_input = input("Let's try this again, How many players?")
            num_players = int(user_input)
            
            if num_players < 1: 
                raise ValueError()
        except ValueError: 
            print('"', user_input, '"', " is not an acceptable number of players. I can do this all day.")
    
    return num_players

def getPlayerNames():
    player_list = []
    while(True):
        userInput = input("Who is playing? Enter a name or leave blank to start:")
        if(userInput != ""):
            player_list.append(str(userInput))
            awardExtremePoints(str(userInput), 0)
        else:
            break
    return player_list
'''
def addPlayersToExtremePointDict(player_list):
    for player in player_list:
        extreme_point_dict[player] = 0
'''

def awardExtremePoints(player, points):
    if (player in extreme_point_dict) == False:
        extreme_point_dict[player] = 0
    extreme_point_dict[player] += points

def printExtremePoints():
    for player, points in extreme_point_dict.items():
        print(str(player)+": "+str(points))

truthList = make_list("Truths.txt")
dareList = make_list("Dares.txt")
quirkList = make_list("Quirks.txt")

def giveTruth():
    global truthList
    global last_was_truth
    last_was_truth = True
    newTruth = truthList.pop()
    newTruth = process(newTruth, player_names)
    print(newTruth)
    category = getCategoryFromDistribution(truthQuirkProbabilityDistribution)    
    while category == 1:
        addQuirk()
        category = getCategoryFromDistribution(truthQuirkProbabilityDistribution)
    if not truthList: 
        print("You've seen all the truths, get ready for more of the same!")
        truthList = make_list("Truths.txt")
       	
def giveDare():
    global dareList
    global last_was_truth
    last_was_truth = False
    newDare = dareList.pop()
    newDare = process(newDare, player_names)
    print(newDare)
    category = getCategoryFromDistribution(dareQuirkProbabilityDistribution)
    while category == 1:
        addQuirk()
        category = getCategoryFromDistribution(dareQuirkProbabilityDistribution)
    if not dareList: 
        print("You've seen all the dares, get ready for more of the same!")
        dareList = make_list("Dares.txt")
        
def addQuirk():
    global quirkList
    newQuirk = quirkList.pop()
    newQuirk = process(newQuirk, player_names)
    print(newQuirk)
    if not quirkList: 
        print("You've seen all the quirks, get ready for more of the same!")
        quirkList = make_list("Quirks.txt")


#Provide boundaries, not proportions
truthQuirkProbabilityDistribution = [0.8, 1.0]
dareQuirkProbabilityDistribution = [0.8, 1.0]

'''
try: 
    user_input = input("Welcome! How many players?")
    num_players = int(user_input)
    
    if num_players < 1: 
        num_players = getNumPlayersAggressively(user_input)
except ValueError: 
    num_players = getNumPlayersAggressively(user_input)
'''

player_names = getPlayerNames()

while True:        
    userInput = ""
    while userInput != "t" and userInput != "d" and userInput != "r" and userInput != "n" and userInput != "s" and userInput != "x" and userInput != "+" and userInput != "-" and userInput != ".":
        userInput = input(str(player_names[current_player]) + ", do you want a Truth (t) or a Dare (d)?")
    
    if userInput == "t":
        giveTruth()
    elif userInput == "d":
        giveDare()
    elif userInput == "r":
        current_player = (current_player - 2) % len(player_names)
    elif userInput == "n":
        current_player = (current_player - 1) % len(player_names)
        print("New challenge for " + str(player_names[current_player]) +":")
        if last_was_truth:
            giveTruth()
        else:
            giveDare()
    elif userInput == "s":
        print("Skipping "+str(player_names[current_player])+"...")
    elif userInput == "x":
        printExtremePoints()
        while(True):
            userInput = input("Award or spend Extreme Points! Type in a name, leave a space, and then a number of points to award or spend (leave blank to continue playing): ")
            if(userInput != ""):
                tokens = userInput.split()
                player = str(tokens[0])
                points = 0
                if len(tokens) == 2:
                    try:
                        points = int(tokens[1])
                    except:
                        print(Exception)
                if player in extreme_point_dict:
                    try:
                        awardExtremePoints(player, points)
                    except:
                        print(str(points)+" is not recognized as a number. Try again, and make sure to leave a space.")
                else:
                    print(player+" is not recognized as a current player. Check the list to make sure your spelling matches.")
            else:
                break
        current_player = (current_player - 1) % len(player_names)
    elif userInput == "+":
        while(True):
            userInput = input("Who is joining? Enter a name or leave blank to continue playing:")
            if(userInput != ""):
                player_names.insert(current_player, str(userInput))
                awardExtremePoints(str(userInput), 0)
            else:
                break
        current_player = (current_player - 1) % len(player_names)
    elif userInput == "-":
        print("Bye, "+str(player_names[current_player])+"! You've been removed from the list of active players.")
        del player_names[current_player]
        if(len(player_names) > 0):
            current_player = (current_player - 1) % len(player_names)
        else:
            print("You're the last to go. Thanks for playing!")
            break
    elif userInput == ".":
        print("Thanks for playing!")
        break
    else:
        print("Something went wrong. Try again please!")
    current_player = (current_player + 1) % len(player_names)
