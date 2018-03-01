from random import *

#user_input = ""
#num_players = ""
current_player = 0

def make_list(fileName):
    sourceFile = open(fileName)
    
    #Taken from http://stackoverflow.com/questions/4842057/python-easiest-way-to-ignore-blank-lines-when-reading-a-file
    lines = (line.rstrip() for line in sourceFile) 
    itemList = list(line for line in lines if line)
    
    shuffle(itemList)
    return itemList

def getCategoryFromDistribution(probabilityDistribution):
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
        else:
            break
    return player_list

truthList = make_list("Truths.txt")
dareList = make_list("Dares.txt")
quirkList = make_list("Quirks.txt")

#Provide boundaries, not proportions
truthProbabilityDistribution = [1.0]
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
    if not truthList: 
        print("You've seen all the truths, get ready for more of the same!")
        truthList = make_list("Truths.txt")
        
    if not dareList: 
        print("You've seen all the dares, get ready for more of the same!")
        dareList = make_list("Dares.txt")
        
    if not quirkList: 
        print("You've seen all the quirks, get ready for more of the same!")
        quirkList = make_list("Quirks.txt")
        
    userInput = "X"
    while userInput != "t" and userInput != "d" and userInput != "r" and userInput != ".":
        userInput = input(str(player_names[current_player]) + ", do you want a Truth (t) or a Dare (d)?")
    randomProbability = uniform(0, 1)
    #print(randomProbability)
    if userInput == "t":
        newTruth = truthList.pop()
        newTruth = process(newTruth, player_names)
        print(newTruth)
    elif userInput == "d":
        category = getCategoryFromDistribution(dareQuirkProbabilityDistribution)
        #print(category)
        if category == 0:
            newDare = dareList.pop()
            newDare = process(newDare, player_names)
            print(newDare)
        elif category == 1:
            newQuirk = quirkList.pop()
            newQuirk = process(newQuirk, player_names)
            print(newQuirk)
        else:
            print("Something went wrong. Try again please!")
    elif userInput == "r":
        current_player = (current_player - 2) % len(player_names)
    elif userInput == ".":
        print("Thanks for playing!")
        break
    else:
        print("Something went wrong. Try again please!")
    current_player = (current_player + 1) % len(player_names)
