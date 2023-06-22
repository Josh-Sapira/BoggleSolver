#Read in list of words
my_file = open("words.txt", "r")
data = my_file.read()
wordsList = data.split("\n")
wordsList = [x.lower() for x in wordsList]
my_file.close()

#Initialize variables
numRows = 4
numCols = 4
presentWords = []
allWords = []

#Check if word is in wordsList (constant time operation)
def isWord(string):
    print(string)
    #return true if found in list, otherwise return false
    if string in wordsList and len(string)>=3:
        return True
    return False

#Check if word is prefix of wordList
def isPrefix(string):
    for word in wordsList:
        if word.startswith(string):
            return True
    return False

#Print results
def printResults(tupleList):
    for triple in tupleList:
        string, root, route = triple
        print(f"{string} starts at {root[0]+1, root[1]+1} and going {route[:-1]}")

#Get direction
def getDirection(i, j, row, col):
    if row==i:
        #Same row
        if col==j-1:
            return "L"
        elif col==j+1:
            return "R"
    elif row==i-1:
        #Up
        if col==j-1:
            return "UL"
        elif col==j:
            return "U"
        elif col==j+1:
            return "UR"
    elif row==i+1:
        #Down
        if col==j-1:
            return "DL"
        elif col==j:
            return "D"
        elif col==j+1:
            return "DR"

#Recursive DFS
def recFindWords(board, visited, i, j, stringTuple):

    #extract info from string for ease of update values
    string, root, route = stringTuple

    #Mark current cell as visited
    visited[i][j] = True

    #append letter to current str
    string += board[i][j]

    #add to list if new word
    if isWord(string) and string not in allWords:
        presentWords.append(stringTuple)
        allWords.append(string)

    #terminate recursion if not a prefix for any word in the list
    if not isPrefix(string):
        visited[i][j] = False
        return
    
    #Traverse adjacent nodes
    row = i-1
    while row <= i+1 and row < numRows:
        col = j-1
        while col <= j+1 and col < numCols:
            if row >= 0 and col >= 0 and not visited[row][col]:
                #Get direction of next step and add to route, carry into recursive call
                dir = getDirection(i, j, row, col)
                newRoute = route + [dir]

                recFindWords(board, visited, row, col, (string, root, newRoute))
            col += 1
        row += 1
    
    #reset str to before the char was added
    string = string[:-1]
    
    #mark node as no longer visited
    visited[i][j] = False

#Function to run the recursion
def findWords(board):
    #Set visited to false everywhere
    visited = [[False for j in range(numCols)] for i in range(numRows)]

    #Run recursion with each node as the root 
    for i in range(numRows):
        for j in range(numCols):
            recFindWords(board, visited, i, j, ("", (i,j), []))


#Prompt for board until valid input received
letters = ""
while len(letters) != 16:
    letters = input("Enter the letters row by row -- top to bottom -- without spaces: ")
    letters = letters.lower()

firstRow = [letters[0], letters[1], letters[2], letters[3]]
secondRow = [letters[4], letters[5], letters[6], letters[7]]
thirdRow = [letters[8], letters[9], letters[10], letters[11]]
fourthRow = [letters[12], letters[13], letters[14], letters[15]]
board = [firstRow, secondRow, thirdRow, fourthRow]

#Find results
findWords(board)

#Print Results
print("The following words are present:\n")
presentWords.sort(key = lambda x: len(x[0]), reverse = True)
printResults(presentWords)
print("A total of", end=" ")
print(len(presentWords), end=" ")
print("words have been found")