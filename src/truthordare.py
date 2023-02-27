from random import *

useQuirks = False
verbose = False

#Provide boundaries, not proportions
truthQuirkProbabilityDistribution = [0.8, 1.0]
dareQuirkProbabilityDistribution = [0.8, 1.0]

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

#Process method using name
def process(line, player_names):
    global player_number
	
    player_number = current_player
	
    while(player_number == current_player):
        player_number = randint(1, len(player_names)) - 1
		
    player_reference = str(player_names[player_number])
    new_line = line.replace("someone", player_reference)
	
    return new_line

def getPlayerNames():
    player_list = []
	
    while(True):
        userInput = input("Who is playing? Enter a name or leave blank to start:")
        if(userInput != ""):
            player_list.append(str(userInput))
            awardExtremePoints(str(userInput), 0)
        elif len(player_list) < 2:
            print("You're going to want at least 2 people for Truth or Dare.")
        else:
            break
    return player_list

def awardExtremePoints(player, points):
    if (player in extreme_point_dict) == False:
        extreme_point_dict[player] = 0
	
    extreme_point_dict[player] += points

def printExtremePoints():
    for player, points in extreme_point_dict.items():
        print(str(player)+": "+str(points))

def giveTruth():
    global truthList
    global last_was_truth
    global useQuirks
    global truthQuirkProbabilityDistribution
	
    last_was_truth = True
    newTruth = truthList.pop()
    newTruth = process(newTruth, player_names)
    print(newTruth)
	
    if useQuirks: 
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
    global useQuirks
    global dareQuirkProbabilityDistribution
	
	
    last_was_truth = False
    newDare = dareList.pop()
    newDare = process(newDare, player_names)
    print(newDare)
	
    if useQuirks: 
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


def main():
    global current_player
    global player_number
    global extreme_point_dict
    global last_was_truth
	
    current_player = 0
    player_number = current_player
    extreme_point_dict = {}
    last_was_truth = False
	
    global truthList
    global dareList
    global quirkList
	
    truthList = make_list("Truths.txt")
    dareList = make_list("Dares.txt")
    quirkList = make_list("Quirks.txt")
	
    if verbose: 
        print("Loaded " + str(len(truthList)) + " truths...")
        print("Loaded " + str(len(dareList)) + " dares...")
        print("Loaded " + str(len(quirkList)) + " quirks...")

    global player_names
	
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

if __name__ == "__main__":
    main()