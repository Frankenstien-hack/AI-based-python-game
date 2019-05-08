import random
import sys
import pygame
import time
import copy 
from pygame.locals import *      #for Quit

FPS = 100
WINDOWHEIGHT = 700
WINDOWWIDTH = 800
BOARDHEIGHT = 10
BOARDWIDTH = 10
SPACESIZE = 60
WHITETILE = 'WHITETILE'
BLACKTILE = 'BLACKTILE'
HINTTILE = 'HINTTILE'
EMPTYSPACE = 'EMPTYSPACE'
ANIMATIONSPEED = 25

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GREEN      = (  0, 155,   0)
BBLUE      = (  0,  50, 255)
BROWN      = (174,  94,   0)

TEXTBGCOLOR1 = BBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

def GetNewBoard():
    #Creates a new board.
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTYSPACE] * BOARDHEIGHT)

    return board

def TranslateBoard(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)

def ResetBoard(board):
    #blanks the board and sets the tiles to their start position.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTYSPACE

    board[4][4] = WHITETILE
    board[4][5] = BLACKTILE
    board[5][4] = BLACKTILE
    board[5][5] = WHITETILE

def IsOnBoard(x, y):
    #Returns true if coordinates are on the board.
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def GetScoreOfBoard(board):
    #Determine the score.
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == WHITETILE:
                xscore += 1
            if board[x][y] == BLACKTILE:
                oscore += 1

    return {WHITETILE:xscore, BLACKTILE:oscore}

def DrawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(BOARDWIDTH + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    # Draw the black & white tiles or hint spots.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = TranslateBoard(x, y)
            if board[x][y] == WHITETILE or board[x][y] == BLACKTILE:
                if board[x][y] == WHITETILE:
                    TileColor = WHITE
                else:
                    TileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, TileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            if board[x][y] == HINTTILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))

def IsValidMove(board, tile, xstart, ystart):
    
    if board[xstart][ystart] != EMPTYSPACE or not IsOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile 

    if tile == WHITETILE:
        OtherTile = BLACKTILE
    else:
        OtherTile = WHITETILE

    TilesToFlip = []
    #Check each directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if IsOnBoard(x, y) and board[x][y] == OtherTile:
            x += xdirection
            y += ydirection
            if not IsOnBoard(x, y):
                continue
            while board[x][y] == OtherTile:
                x += xdirection
                y += ydirection
                if not IsOnBoard(x, y):
                    break
            if not IsOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    TilesToFlip.append([x, y])

    board[xstart][ystart] = EMPTYSPACE
    if len(TilesToFlip) == 0: 
        return False
    
    return TilesToFlip

def IsOnCorner(x, y):
    #Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == BOARDWIDTH and y == 0) or \
           (x == 0 and y == BOARDHEIGHT) or \
           (x == BOARDWIDTH and y == BOARDHEIGHT)

def IsOnEdge(x,y):
    return (x == 1 and y == 0) or \
           (x == BOARDWIDTH and y == 1) or \
           (x == 1 and y == BOARDHEIGHT) or \
           (x == 0 and y == 1) or \
           (x == 2 and y == 0) or \
           (x == BOARDWIDTH and y == 2) or \
           (x == 2 and y == BOARDHEIGHT) or \
           (x == 0 and y == 2) or \
           (x == 3 and y == 0) or \
           (x == BOARDWIDTH and y == 3) or \
           (x == 3 and y == BOARDHEIGHT) or \
           (x == 0 and y == 3) or \
           (x == 4 and y == 0) or \
           (x == BOARDWIDTH and y == 4) or \
           (x == 4 and y == BOARDHEIGHT) or \
           (x == 0 and y == 4) or \
           (x == 5 and y == 0) or \
           (x == BOARDWIDTH and y == 5) or \
           (x == 5 and y == BOARDHEIGHT) or \
           (x == 0 and y == 5) or \
           (x == 6 and y == 0) or \
           (x == BOARDWIDTH and y == 6) or \
           (x == 6 and y == BOARDHEIGHT) or \
           (x == 0 and y == 6) or \
           (x == 7 and y == 0) or \
           (x == BOARDWIDTH and y == 7) or \
           (x == 7 and y == BOARDHEIGHT) or \
           (x == 0 and y == 7) or \
           (x == 8 and y == 0) or \
           (x == BOARDWIDTH and y == 8) or \
           (x == 8 and y == BOARDHEIGHT) or \
           (x == 0 and y == 8) or \
           (x == 9 and y == 0) or \
           (x == BOARDWIDTH and y == 9) or \
           (x == 9 and y == BOARDHEIGHT) or \
           (x == 0 and y == 9)

def GetValidMoves(board, tile):
    #Returns a list of (x,y)tuples of all valid moves.
    ValidMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if IsValidMove(board, tile, x, y) != False:
                ValidMoves.append((x, y))
    
    return ValidMoves

def GetBoardWithValidMoves(board, tile):
    #Returns a new board with hint markings.
    DuplicateBoard = copy.deepcopy(board)
    for x, y in GetValidMoves(DuplicateBoard, tile):
        DuplicateBoard[x][y] = HINTTILE
    
    return DuplicateBoard

def DrawInfo(board, PlayerTile, ComputerTile, turn):
    #Draws scores and whose turn it is at the bottom of the screen.
    scores = GetScoreOfBoard(board)
    ScoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[PlayerTile]), str(scores[ComputerTile]), turn.title()), True, TEXTCOLOR)
    ScoreRect = ScoreSurf.get_rect()
    ScoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(ScoreSurf, ScoreRect)

def GetSpaceClicked(mousex, mousey):
    #Return a tuple of two integers of the board space coordinates where the mouse was clicked.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if mousex > x * SPACESIZE + XMARGIN and \
                mousex < (x + 1) * SPACESIZE + XMARGIN and \
                mousey > y * SPACESIZE + YMARGIN and \
                mousey < (y + 1) * SPACESIZE + YMARGIN:
                return (x, y)
    
    return None

def AnimateTileChange(TilesToFlip, TileColor, AdditionalTile):
    
    if TileColor == WHITETILE:
        AdditionalTileColor = WHITE
    else:
        AdditionalTileColor = BLACK
    AdditionalTileX, AdditionalTileY = TranslateBoard(AdditionalTile[0], AdditionalTile[1])
    pygame.draw.circle(DISPLAYSURF, AdditionalTileColor, (AdditionalTileX, AdditionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if TileColor == WHITETILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif TileColor == BLACKTILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in TilesToFlip:
            centerx, centery = TranslateBoard(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        CheckForQuit()

def EnterPlayerTile():

    TextSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    TextRect = TextSurf.get_rect()
    TextRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 40)

    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        CheckForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [WHITETILE, BLACKTILE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [BLACKTILE, WHITETILE]

        # Draw the screen.
        DISPLAYSURF.blit(TextSurf, TextRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def MakeMove(board, tile, xstart, ystart, RealMove=False):
    TilesToFlip = IsValidMove(board, tile, xstart, ystart)

    if TilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if RealMove:
        AnimateTileChange(TilesToFlip, tile, (xstart, ystart))

    for x, y in TilesToFlip:
        board[x][y] = tile
    
    return True

def GetComputerMove(board, ComputerTile):
    PossibleMoves = GetValidMoves(board, ComputerTile)
    
    random.shuffle(PossibleMoves)
    #Always go for a corner if available.
    for x, y in PossibleMoves:
        if IsOnCorner(x, y):
            return [x, y]
    for x, y in PossibleMoves:
        if IsOnEdge(x, y):
            return [x, y]

    #Go through all possible moves and remember the best scoring move
    BestScore = -1
    for x, y in PossibleMoves:
        DuplicateBoard = copy.deepcopy(board)
        MakeMove(DuplicateBoard, ComputerTile, x, y)
        score = GetScoreOfBoard(DuplicateBoard)[ComputerTile]
        if score > BestScore:
            BestMove = [x, y]
            BestScore = score
    
    return BestMove

'''def MinMax(board,ComputerTile,depth,maxDepth):
    if (depth == maxDepth):
        return [GetScoreOfBoard(board)[ComputerTile],None]

    BestMove = None

    PossibleMoves = GetValidMoves(board, ComputerTile)
   # for x, y in PossibleMoves:
    #    if IsOnCorner(x, y):
     #       return [x, y]

    BestScore = 999999999

    for x,y in PossibleMoves:
        newBoard = copy.deepcopy(board)
        MakeMove(newBoard,ComputerTile,x,y)
        [score,BestMove] = MinMax(newBoard,ComputerTile,depth+1,maxDepth)
            
        if score < BestScore:
            BestMove = [x,y]
            BestScore = score
            
    return [BestScore,BestMove]'''

def CheckForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == KESCAPE):
            pygame.quit()
            sys.exit()

def RunGame():
    MainBoard = GetNewBoard()
    ResetBoard(MainBoard)
    ShowHints = False
    turn = random.choice(['computer', 'player'])

    # Draw the starting board and ask the player what color they want.
    DrawBoard(MainBoard)
    PlayerTile, ComputerTile = EnterPlayerTile()

    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    NewGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    NewGameRect = NewGameSurf.get_rect()
    NewGameRect.topright = (WINDOWWIDTH - 8, 10)
    HintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    HintsRect = HintsSurf.get_rect()
    HintsRect.topright = (WINDOWWIDTH - 8, 40)

    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            # Player's turn:
            if GetValidMoves(MainBoard, PlayerTile) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if ShowHints:
                    BoardToDraw = GetBoardWithValidMoves(MainBoard, PlayerTile)
                else:
                    BoardToDraw = MainBoard

                CheckForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if NewGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        elif HintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            ShowHints = not ShowHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = GetSpaceClicked(mousex, mousey)
                        if movexy != None and not IsValidMove(MainBoard, PlayerTile, movexy[0], movexy[1]):
                            movexy = None

                # Draw the game board.
                DrawBoard(BoardToDraw)
                DrawInfo(BoardToDraw, PlayerTile, ComputerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(NewGameSurf, NewGameRect)
                DISPLAYSURF.blit(HintsSurf, HintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            MakeMove(MainBoard, PlayerTile, movexy[0], movexy[1], True)
            if GetValidMoves(MainBoard, ComputerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            # Computer's turn:
            if GetValidMoves(MainBoard, ComputerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            # Draw the board.
            DrawBoard(MainBoard)
            DrawInfo(MainBoard, PlayerTile, ComputerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(NewGameSurf, NewGameRect)
            DISPLAYSURF.blit(HintsSurf, HintsRect)

            # Make it look like the computer is thinking by pausing a bit.
            PauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < PauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            x, y = GetComputerMove(MainBoard, ComputerTile)
            MakeMove(MainBoard, ComputerTile, x, y, True)
            if GetValidMoves(MainBoard, PlayerTile) != []:
                # Only set for the player's turn if they can make a move.
                turn = 'player'

    # Display the final score.
    DrawBoard(MainBoard)
    scores = GetScoreOfBoard(MainBoard)

    # Determine the text of the message to display.
    if scores[PlayerTile] > scores[ComputerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % \
               (scores[PlayerTile] - scores[ComputerTile])
    elif scores[PlayerTile] < scores[ComputerTile]:
        text = 'You lost. The computer beat you by %s points.' % \
               (scores[ComputerTile] - scores[PlayerTile])
    else:
        text = 'The game was a tie!'

    TextSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    TextRect = TextSurf.get_rect()
    TextRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(TextSurf, TextRect)

    # Display the "Play again?" text with Yes and No buttons.
    Text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    Text2Rect = Text2Surf.get_rect()
    Text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    # Make "Yes" button.
    YesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    YesRect = YesSurf.get_rect()
    YesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    # Make "No" button.
    NoSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    NoRect = NoSurf.get_rect()
    NoRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        CheckForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if YesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif NoRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(TextSurf, TextRect)
        DISPLAYSURF.blit(Text2Surf, Text2Rect)
        DISPLAYSURF.blit(YesSurf, YesRect)
        DISPLAYSURF.blit(NoSurf, NoRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if TileColor == WHITETILE:
        AdditionalTileColor = WHITE
    else:
        AdditionalTileColor = BLACK
    AdditionalTileX, AdditionalTileY = TranslateBoard(AdditionalTile[0], AdditionalTile[1])
    pygame.draw.circle(DISPLAYSURF, AdditionalTileColor, (AdditionalTileX, AdditionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if TileColor == WHITETILE:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif TileColor == BLACKTILE:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in TilesToFlip:
            centerx, centery = TranslateBoard(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        CheckForQuit()


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('AI Game')
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 40)

    #Set up the background image.
    BoardImage = pygame.image.load('board.jpg')
    BoardImage = pygame.transform.smoothscale(BoardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    BoardImageRect = BoardImage.get_rect()
    BoardImageRect.topleft = (XMARGIN, YMARGIN)

    BGIMAGE = pygame.image.load('background.png')
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(BoardImage, BoardImageRect)

    #Run the main game.
    while True:
        if RunGame() == False:
            break

if __name__ == '__main__':
    main()