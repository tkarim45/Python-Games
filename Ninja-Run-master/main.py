

# Imports all pngs for program
background = "Screens/background.png"
cobble = "Screens/cobblepath713.png"
hitscreen = "Screens/splash_hit.png"
frontScreen = "Screens/FrontScreen.png"
scoreBG = "Screens/highscorepage.png"
userNamein = "Screens/usernamein.png"

helpscrn = "Screens/helpscreen.png"
spaceUP = "Keys/spaceUP.png"
spaceDOWN = "Keys/spaceDOWN.png"
helpBtn = "Buttons/bambooHELP.png"

playBtn = "Buttons/bambooPLAY.png"
backBtn = "Buttons/bambooBACK.png"
highS = "Buttons/bambooHIGHS.png"

pngE = "Buttons/bambooEASY.png"
pngM = "Buttons/bambooMEDIUM.png"
pngH = "Buttons/bambooHARD.png"

ninja1 = "ninja/ninja1.png"
ninja2 = "ninja/ninja2.png"
ninja3 = "ninja/ninja3.png"
ninja4 = "ninja/ninja4.png"
ninja5 = "ninja/ninja5.png"
ninja6 = "ninja/ninja6.png"
ninja7 = "ninja/ninja7.png"
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \
        

import pygame, sys, random
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Ninja Run')
basicFont = pygame.font.SysFont(None, 25)
WHITE = (255, 255, 255)
HSBROWN = (182, 114, 78)

# Modes for each game difficulty # Numbers may be changed
easy = [("bgSpeed",50),("jumpSpeed",200),("boxSpeed", 100)]
medium = [("bgSpeed",75),("jumpSpeed",250),("boxSpeed", 150)]
hard = [("bgSpeed",150),("jumpSpeed",300),("boxSpeed", 350)]
difficulty = [easy,medium,hard]
loadFile = "highscore_DATA/highscoreEASY.txt" # Original difficulty is set to easy so highscores go in easy csv file

# Sets screen size
WINDOWHEIGHT = 450
WINDOWWIDTH = 800
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)

# / / / / / / / / / / / / / / / / / / / / Converts pngs to pygame format
#  / / / / / / / / / / / / / / / / / / /

bg = pygame.image.load(background).convert()
cobblePath = pygame.image.load(cobble).convert()
pngEasy = pygame.image.load(pngE).convert_alpha()
pngMed = pygame.image.load(pngM).convert_alpha()
pngHard = pygame.image.load(pngH).convert_alpha()
hitscreenPath = pygame.image.load(hitscreen).convert()
frontPage = pygame.image.load(frontScreen).convert()
playButton = pygame.image.load(playBtn).convert_alpha()
highButton = pygame.image.load(highS).convert_alpha()
backButton = pygame.image.load(backBtn).convert_alpha()
highscoreBG = pygame.image.load(scoreBG).convert()
usernameBG = pygame.image.load(userNamein).convert()
helpBG = pygame.image.load(helpscrn).convert()
spacebarDOWN = pygame.image.load(spaceDOWN).convert()
spacebarUP = pygame.image.load(spaceUP).convert()
helpButton = pygame.image.load(helpBtn).convert_alpha()



# / / / / / / / / / / / / / / / / / Ninja animation picture convert
ninja_1 = pygame.image.load(ninja1).convert_alpha()
ninja_2 = pygame.image.load(ninja2).convert_alpha()
ninja_3 = pygame.image.load(ninja3).convert_alpha()
ninja_4 = pygame.image.load(ninja4).convert_alpha()
ninja_5 = pygame.image.load(ninja5).convert_alpha()
ninja_6 = pygame.image.load(ninja6).convert_alpha()
ninja_7 = pygame.image.load(ninja7).convert_alpha()
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \

# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \
#\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \

#Loads and plays track in a continuous loop
'''
pygame.mixer.music.load("music/song1.mp3")
pygame.mixer.music.play(-1, 0.1)
'''
#

# / / / / / / / / / / / / / / / / / / / / Sets in-game variables
clock = pygame.time.Clock()
undivScore = 0
currentScore = 0

bgX = 0
bgSpeed = 50
cobblePathX = 0

x = 75
y = 360
movey = 0

maxHeight = 100
jumpSpeed = 200
time = 0
timeTemp = 0
sec = 0
fin = False

boxParameters = [("Height",200),("Width",50)]
colour = (150,75,0)
newBox = True
points = [(-100,0),(-100,0),(-100,0),(-100,0)]
boxSpeed = 100
nextBox = 0
hitObject = False

playAgain = False
highScores = False
highscoreScreen = False
helpScreen = False
keyDown = False
gamePause = False
gameMode = 0
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \

# / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / # Highscore section
userName = ""
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass
    
def READ_SCORES():
    highscoreList = [[],[],[]]
    textRead = open(loadFile,"r")
    for line in textRead:
        row = line.split(',')
        highscoreList[0].append(row[0])
        highscoreList[1].append(row[1])
        highscoreList[2].append(row[2])
    return(highscoreList)

def NEW_SCORE(highscoreList,currentScore):
    global newPos
    newPos = 10
    for i in reversed(range(0,len(highscoreList[0]))):
        if currentScore > int(highscoreList[2][i]):
            newPos = highscoreList[0][i]
    return(newPos)
   
def NEW_HIGHSCORE(highscoreList,currentScore,newPos,userName):
    for i in reversed(range(int(newPos),len(highscoreList[0]))):
        highscoreList[1][i] = highscoreList[1][i - 1]
        highscoreList[2][i] = highscoreList[2][i - 1]
    highscoreList[1][newPos - 1] = userName
    highscoreList[2][newPos - 1] = currentScore
    return(highscoreList)

def WRITE_HIGHSCORE(highscoreList):
    textWrite = open(loadFile,"w")
    textWrite.write("")
    textAppend = open(loadFile,"a")
    for i in range(0,len(highscoreList[0])):
        line = str(highscoreList[0][i]) + ',' + highscoreList[1][i] + ',' + str(highscoreList[2][i]) + ',\n'
        textAppend.write(line)

def ALL_SCORES():
    fullhighscoreList = [[[],[],[]],[[],[],[]],[[],[],[]]]
    for i in range(0,3):
        if i == 0:
            loadFile = "Highscore_DATA/highscoreEASY.txt"
        elif i == 1:
            loadFile = "Highscore_DATA/highscoreMEDIUM.txt"
        elif i == 2:
            loadFile = "Highscore_DATA/highscoreHARD.txt"
        textRead = open(loadFile,"r")
        for line in textRead:
            row = line.split(',')
            fullhighscoreList[i][0].append(row[0])
            fullhighscoreList[i][1].append(row[1])
            fullhighscoreList[i][2].append(row[2])
    return(fullhighscoreList)

fullhighscoreList = ALL_SCORES()
# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ # Highscore section


def RANDOM_BOX(boxParameters):
    randY = random.randint(50,boxParameters[0][1])
    randX = random.randint(10,boxParameters[1][1])
    point1_1 = WINDOWWIDTH + boxParameters[1][1] - randX
    point1_2 = WINDOWHEIGHT - 30 - randY
    point1 = (point1_1,point1_2)
    point3_1 = WINDOWWIDTH + boxParameters[1][1]
    point3_2 = WINDOWHEIGHT - 30
    point3 = (point3_1,point3_2)
    point2_1 = WINDOWWIDTH + boxParameters[1][1]
    point2_2 = WINDOWHEIGHT - 30 - randY
    point2 = (point2_1,point2_2)
    point4_1 = WINDOWWIDTH + boxParameters[1][1] - randX
    point4_2 = WINDOWHEIGHT - 30
    point4 = (point4_1,point4_2)
    points = [point1,point2,point3,point4]
    return(points)

def BOX_MOVE(points,boxm):
    pointTemp = []
    for i in range(0,4):
        pointX = points[i][0]
        pointX -= boxm
        pointY = points[i][1]
        pointTemp.append((pointX,pointY))
    return(pointTemp)

while True:
    if gamePause == False:
        ms = clock.tick()
        secs = ms / 1000.0
        dm = secs * jumpSpeed
        time += dm
        bm = secs * bgSpeed
        boxm = secs * boxSpeed
        sec += secs
        if sec > 0.5:
            sec = 0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and playAgain == False:
            x1,y1 = pygame.mouse.get_pos()
            if 500 < x1 < 752:
                if 300 < y1 < 403 and highscoreScreen == False:
                    undivScore = 0
                    playAgain = True
                    hitObject = False
                    timeTemp = 0
                elif 175 < y1 < 278 and highscoreScreen == False:
                    highscoreScreen = True
                elif 50 < y1 < 153:
                    helpScreen = True
                    
            if 0 < x1 < 126:
                if 401 < y1 < 450:
                    if highscoreScreen:
                        highscoreScreen = False
                    elif helpScreen:
                        helpScreen = False
            
            if highscoreScreen == False and helpScreen == False:
                if 0 < x1 < 100:
                    if 0 < y1 < 35:
                        bgSpeed = difficulty[0][0][1]
                        jumpSpeed = difficulty[0][1][1]
                        boxSpeed = difficulty[0][2][1]
                        loadFile = "Highscore_DATA/highscoreEASY.txt"
                        gameMode = 0

                elif 100 < x1 < 200:
                    if 0 < y1 < 35:
                        bgSpeed = difficulty[1][0][1]
                        jumpSpeed = difficulty[1][1][1]
                        boxSpeed = difficulty[1][2][1]
                        loadFile = "Highscore_DATA/highscoreMEDIUM.txt"
                        gameMode = 1

                elif 200 < x1 < 300:
                    if 0 < y1 < 35:
                        bgSpeed = difficulty[2][0][1]
                        jumpSpeed = difficulty[2][1][1]
                        boxSpeed = difficulty[2][2][1]
                        loadFile = "Highscore_DATA/highscoreHARD.txt"
                        gameMode = 2

        if event.type == KEYDOWN:
            if event.key == K_SPACE and playAgain:
                if y > 359:
                    if y > maxHeight:
                        movey = True
                    else:
                        movey = False
            elif event.key == K_SPACE and helpScreen:
                keyDown = True
                
        if event.type == KEYUP: # allows user to jump up and down in game
            if event.key == K_SPACE and playAgain:
                movey = False
            elif event.key == K_SPACE and playAgain == False and highscoreScreen == False and helpScreen == False:
                undivScore = 0
                playAgain = True
                hitObject = False
                timeTemp = 0
            elif event.key == K_SPACE and helpScreen:
                keyDown = False
            elif event.key == K_ESCAPE:
                playAgain = False


    if playAgain:
        undivScore += secs * 10
        currentScore = int(undivScore // 1)
        currentScoreDisplay = basicFont.render('Score: ' + str(currentScore), True, WHITE, HSBROWN)
        currentScoreB = currentScoreDisplay.get_rect()
        
        if movey == True and y > maxHeight and fin == True: # Increases sprite height
            y -= dm
        elif movey == False and y < 360: # Decreases sprite height
            y += dm / 2
        else: # Prevents user jumping in mid air
            fin = False
            if time > 1:
                if y < 360:
                    y += dm / 2
                else:
                    fin = True
            else:
                y = y

        bgX -= bm  # Moves background
        if bgX < -1600:
            bgX = 0

        cobblePathX -= boxm  # Moves path at bottom of screen
        if cobblePathX < -713:
            cobblePathX = 0

        screen.blit(bg, (bgX, 0))  # Back layer
        if sec < 0.07142857142857142857142857142857:
            screen.blit(ninja_1, (x, y))
        elif 0.07142857142857142857142857142857 < sec < 0.14285714285714285714285714285714:
            screen.blit(ninja_2, (x, y))
        elif 0.14285714285714285714285714285714 < sec < 0.21428571428571428571428571428571:
            screen.blit(ninja_3, (x, y))
        elif 0.21428571428571428571428571428571 < sec < 0.28571428571428571428571428571429:
            screen.blit(ninja_4, (x, y))
        elif 0.28571428571428571428571428571429 < sec < 0.35714285714285714285714285714286:
            screen.blit(ninja_5, (x, y))
        elif 0.35714285714285714285714285714286 < sec < 0.42857142857142857142857142857143:
            screen.blit(ninja_6, (x, y))
        elif 0.42857142857142857142857142857143 < sec < 0.5:
            screen.blit(ninja_7, (x, y))
            
        if points[0][0] < -50: # If box is off the screen it orders a new box to be created
            newBox = True
            
        if newBox == False:
            screen.lock()
            pygame.draw.polygon(screen, colour, points)
            screen.unlock()
            points = BOX_MOVE(points,boxm)
            
        elif newBox == True:
            points = RANDOM_BOX(boxParameters)
            newBox = False
            
        screen.blit(cobblePath, (cobblePathX,420))
        screen.blit(currentScoreDisplay, (800 - currentScoreB.width, 0)) # Front layer
        if points[0][0] < x + 30 < points[1][0]: # Checks if user has his box
            if y + 30 > points[0][1]:
                hitObject = True
                
        if hitObject == True:
            screen.blit(hitscreenPath, (0,0))
            timeTemp += secs
            if timeTemp > 2 and hitObject == True: # Times how long hit screen is shown for
                playAgain = False
                highscoreList = READ_SCORES()
                newPos = NEW_SCORE(highscoreList,currentScore)
                newPos = int(newPos)
                if newPos != 10:
                    highScores = True


    elif highScores:
        current_string = []
        userName = ""
        while True:
            screen.blit(usernameBG, (0,0))
            inputDisplay = basicFont.render('Username: ' + str(userName), True, WHITE, HSBROWN)
            screen.blit(inputDisplay,(WINDOWWIDTH/2 - 100,WINDOWHEIGHT/2 - 20))
            if len(current_string) > 4:
                lenDisplay = basicFont.render('Username is too long!', True, WHITE, HSBROWN)
                lenDisplayRect = lenDisplay.get_rect()
                screen.blit(lenDisplay,(WINDOWWIDTH / 2 - 100,WINDOWHEIGHT / 2 - 40))
            pygame.display.update()
            inkey = get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_RETURN:
                if len(current_string) < 5:
                    break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))
            screen.blit(inputDisplay,(WINDOWWIDTH/2,WINDOWHEIGHT/2))
            userName = ""
            for i in current_string:
                userName += i
        highscoreList = NEW_HIGHSCORE(highscoreList,currentScore,newPos,userName)
        WRITE_HIGHSCORE(highscoreList)
        highScores = False
    elif highscoreScreen:
        fullhighscoreList = ALL_SCORES()
        screen.blit(highscoreBG, (0,0))
        backButtonRect = backButton.get_rect()
        screen.blit(backButton, (0,WINDOWHEIGHT - 50))
        easyDisplay = basicFont.render('Easy', True, WHITE, HSBROWN)
        diffLen = easyDisplay.get_rect()
        mediumDisplay = basicFont.render('Medium', True, WHITE, HSBROWN)
        diffLen = mediumDisplay.get_rect()
        hardDisplay = basicFont.render('Hard', True, WHITE, HSBROWN)
        diffLen = hardDisplay.get_rect()
        numDisplay = basicFont.render('#', True, WHITE, HSBROWN)
        numDisRect = numDisplay.get_rect()
        nameDisplay = basicFont.render('Name', True, WHITE, HSBROWN)
        nameDisRect = nameDisplay.get_rect()
        scoreDisplay = basicFont.render('Score', True, WHITE, HSBROWN)
        scoreDisRect = scoreDisplay.get_rect()
        for j in range(0,3):
            for i in range(0,5):
                lenscore0Display = basicFont.render(str(fullhighscoreList[j][0][i]), True, WHITE, HSBROWN)
                numRect = lenscore0Display.get_rect()
                lenscore1Display = basicFont.render(str(fullhighscoreList[j][1][i]), True, WHITE, HSBROWN)
                nameRect = lenscore1Display.get_rect()
                lenscore2Display = basicFont.render(str(fullhighscoreList[j][2][i]), True, WHITE, HSBROWN)
                scoreRect = lenscore2Display.get_rect()
                screen.blit(easyDisplay, (110,110))
                screen.blit(mediumDisplay, (110 + 177,110))
                screen.blit(hardDisplay, (110 + 2 * 177,110))
                screen.blit(numDisplay, (110 + (j* 177),130))
                screen.blit(nameDisplay, (110 + numRect.width + 7 + (j* 177),130))
                screen.blit(scoreDisplay, (110 + 130 + numRect.width + 7 - scoreDisRect.width + (j* 177),130))
                screen.blit(lenscore0Display, (110 + (j* 177), i * 20 + 150))
                screen.blit(lenscore1Display, (110 + numRect.width + 7 + (j* 177), i * 20 + 150))
                screen.blit(lenscore2Display, (110 + 130 + numRect.width + 7 - scoreRect.width + (j* 177), i * 20 + 150))

    elif helpScreen:
        screen.blit(helpBG, (0,0))
        if keyDown:
            screen.blit(spacebarDOWN, (150,350))
        else:
            screen.blit(spacebarUP ,(150,350))
        backButtonRect = backButton.get_rect()
        screen.blit(backButton, (0,WINDOWHEIGHT - 50))
        
    else:
        screen.blit(frontPage, (0,0)) # Displays front page
        screen.blit(playButton, (500,300))
        screen.blit(highButton, (500,175))
        screen.blit(helpButton, (500,50))
        screen.blit(pngEasy, (0,0))
        screen.blit(pngMed, (100,0))
        screen.blit(pngHard, (200,0))

    pygame.display.update()
