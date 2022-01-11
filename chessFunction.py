from Piece import *
def appatientliste(board, name):
    if name in board:
        return True
    else:
        return False


def lettreChiffreLetre(a):
    if a == "a":
        return 0
    if a == "b":
        return 1
    if a == "c":
        return 2
    if a == "d":
        return 3
    if a == "e":
        return 4
    if a == "f":
        return 5
    if a == "g":
        return 6
    if a == "h":
        return 7


def realPs(a):
    if a == 8:
        return 0
    if a == 7:
        return 1
    if a == 6:
        return 2
    if a == 5:
        return 3
    if a == 4:
        return 4
    if a == 3:
        return 5
    if a == 2:
        return 6
    if a == 1:
        return 7

class EchecExeption(Exception):
    pass

def separateurFichier():
    return "  |-----|-----|-----|-----|-----|-----|-----|-----|"


def enPassantGauche(board, pion):
    position = pion.getMaPosition()
    if isinstance((board[position[0]][position[1]-1]),Pawn):
        return True
    else:
        return False
def enPassantDroite(board, pion):
    position = pion.getMaPosition()

    if isinstance((board[position[0]][position[1]+1]),Pawn):
        return True
    else:
        return False


def gamestate(listPiece):
    board = []
    for piece in listPiece:
        position = piece.getMaPosition()
        board[position[0]][position[1]] = piece
    return board


def afficheBoard(board,type):
    list = [8, 7, 6, 5, 4, 3, 2, 1]
    if type == "unicode" :
        l = ""
        l += "   a   b   c   d   e   f   g   h  \n"
        s = ""
        for i in range(8):
            s += str(list[i]) + " "
            for j in range(8):
                if board[i][j] == None:
                    if i%2==1:
                        if j%2==0:
                            s += " " +"\u25FC"+"  "
                        else:
                            s += " " +"\u25FB"+"  "
                    if i%2==0 :
                        if j%2==0:
                            s += " " + "\u25FB" + "  "
                        else :
                             s += " " + "\u25FC" + "  "
                else:
                    s += " " + board[i][j].unicode() + "  "

            s +="\n"
        return l+s

    l = ""
    l += "  |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |"
    l += "\n" + separateurFichier() + "\n"
    s = ""
    for i in range(8):

        s += str(list[i]) + " "
        for j in range(8):
            if board[i][j] == None:
                s += "| " + "  " + "  "
            else:
                s += "| " + str(board[i][j]) + "  "

        s += "|" + "\n"
        c = separateurFichier()
        s += c + "\n"

    return l+s

def timesUp(color,fichier):
    print("Time is up  !!!!")
    print(color+" won  !!!!")
    fichier.write("Time is up !!!!\n"+color+" won  !!!!\n")

def resign (color , fichier):
    if color == "b":
        print("You resign !")
        print ("White won ")
        fichier.write("You resign !\nWhite won.")
    else :
        print("You resign !")
        print("Black won.")
        fichier.write("You resign !\nBlack won.")


def drawing(fichier):
    print("You draw !")
    print("The game is tied.")
    fichier.write("You draw  !\nThe game is tied.")



def configuration (line, board):
    r = line.strip()
    ligne = r.split("-")
    l = list(ligne[0])
    position = change_stringToPosition(ligne[1].lstrip())
    if l[1]=="p" :
        piece=Pawn(position,l[0])
    elif l[1]=="k":
        piece = Knight(position,l[0])
    elif l[1] == "K":
        piece = King(position,l[0])
    elif l[1] == "Q":
        piece = Queen(position,l[0])
    elif l[1] == "b":
        piece = Bishop(position,l[0])
    else :
        piece = Rook(position,l[0])
    board[position[0]][position[1]] = piece


def change_stringToPosition(pos):
    l = list(pos)
    try :
        if len(l)!=2:
            raise EchecExeption
        enchiffre = lettreChiffreLetre(l[0])
        piecePos = (realPs(int(l[1])), enchiffre)
    except EchecExeption as e:
        print("********* Erreur sur la position *********")
    return piecePos


def verifPetitRoque(board, color):
    indice = [5,6]
    if color == "w":
        for i in indice:
            if board[7][i]!=None :
                return False
        return True

    if color == "b":
        for i in indice:
            if board[0][i] != None:
                return False
        return True

def verifGrandroque(board, color):
    indice = [1,2,3]
    if color == "w":
        for i in indice:
            if board[7][i]!=None :
                return False
        return True

    if color == "b":
        for i in indice:
            if board[0][i] != None:
                return False
        return True

def castling(board , destination , position, color):
    if destination== "Petitroque" :
        if color == "b":
            if board[position[0]][position[1]].getName() == "K" and position[0] == 0 and position[1] == 4 and board[0][7].getName() == "r":
                if verifPetitRoque(board, "b") == True:
                    # change position roi
                    board[0][6] = board[position[0]][position[1]]
                    board[position[0]][position[1]] = None
                    board[0][6].setMaposition((0, 6))
                    # change position du roque (tour)
                    board[0][5] = board[0][7]
                    board[0][5].setMaposition((0, 5))
                    board[0][7] = None
                    return board
        if color =="w":
            if board[position[0]][position[1]].getName() == "K" and position[0] == 7 and position[1] == 4 and board[7][7].getName() == "r":
                if verifPetitRoque(board, "w") == True:
                    # change position roi
                    board[7][6] = board[position[0]][position[1]]
                    board[position[0]][position[1]] = None
                    board[7][6].setMaposition((7, 6))
                    # change position du roque (tour)
                    board[7][5] = board[7][7]
                    board[7][5].setMaposition((0, 5))
                    board[7][7] = None
                    return board
    ####  Grand  roque castling #########
    elif destination == "Grandroque" :
        if color =="b":
            if board[position[0]][position[1]].getName() == "K" and position[0] == 0 and position[1] == 4 and board[0][0].getName() == "r":
                if verifGrandroque(board, "b") == True:
                    board[0][2] = board[position[0]][position[1]]
                    board[position[0]][position[1]] = None
                    board[0][2].setMaposition((0, 2))
                    # change position du roque (tour)
                    board[0][3] = board[0][0]
                    board[0][3].setMaposition((0, 3))
                    board[0][0] = None
                    return board
        if color =="w":
            if board[position[0]][position[1]].getName() == "K" and position[0] == 7 and position[1] == 4 and board[7][0].getName() == "r":
                if verifGrandroque(board, "w") == True:
                    board[7][2] = board[position[0]][position[1]]
                    board[position[0]][position[1]] = None
                    board[7][2].setMaposition((7, 2))
                    # change position du roque (tour)
                    board[7][3] = board[7][0]
                    board[7][3].setMaposition((7, 3))
                    board[7][0] = None
                    return board


def detectEchec(board,color):
    roiNoir = None
    roiBlanc = None
    #verifie si le roi noir est enchec
    for i in range(8):
        for j in range (8):
            piece = board[i][j]
            if piece != None and piece.getColor() == "w" and piece.getName()=="K":
                roiBlanc = piece
            if piece != None and piece.getColor() == "b" and piece.getName() == "K":
                roiNoir= piece

    if color == "b":
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece !=None and piece.getColor()=="w":
                    if roiNoir in piece.legalMoves(board):
                         return True
    if color == "w":
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != None and piece.getColor() == "b":
                    if roiBlanc in piece.legalMoves(board):
                        return True
    return False

def stringforPgn(piece):
    if piece.getName()=="k":
        return "N"
    if piece.getName()=="p":
        return ""
    return piece.getName().upper()