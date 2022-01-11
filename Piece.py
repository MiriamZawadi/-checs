
# verif si un pion est en diagonale d'u pion (pion)
def pionDagonale(board, self):
    position = []
    positionPion = self.getMaposition()
    if positionPion[0]+1<8 and positionPion[1]+1<8:
        if self.getColor()== "b":
            if board[positionPion[0]+1][positionPion[1]-1] !=None and board[positionPion[0]+1][positionPion[1]-1].getColor()=="w":
                position.append((positionPion[0]+1, positionPion[1]-1))
            if board[positionPion[0]+1][positionPion[1]+1] != None and board[positionPion[0]+1][positionPion[1]+1].getColor()=="w":
                     position.append((positionPion[0] + 1, positionPion[1]+1))

        if self.getColor() == "w":
            if board[positionPion[0] -1][positionPion[1] - 1] != None and board[positionPion[0]-1][positionPion[1] -1].getColor() == "b":
                position.append((positionPion[0] -1, positionPion[1] - 1))
            if board[positionPion[0] -1][positionPion[1] + 1] != None and board[positionPion[0]-1][positionPion[1] +1].getColor() == "b":
                position.append((positionPion[0] -1, positionPion[1] + 1))
    return position

# classe mere de toutes les pièces
class Piece(object):
    # poisiton est un couple
    maPosition = ()
    enemie = False  # si la pièce à  position precedente etait un ennemi

    # color b ou w
    def __init__(self, position, color):
        self.maPosition = position
        self.color = color

    def getMaPosition(self):
        return self.maPosition

    def getColor(self):
        return self.color

    # dest est la position de destination donc un couple (ligne,colonne)
    # boar c'est le tableau 8x8
    def make_move(self, board, dest):
        if board[dest[0]][dest[1]] != None:
            self.enemie = False

        board[dest[0]][dest[1]] = self
        board[self.maPosition[0]][self.maPosition[1]] = None
        # on met la nouvelle position
        self.maPosition = dest

    # retourne vrai si la nouvelle position n'est pas occupé ou occupé par un ennemi
    #
    # newPosition est un couple(ligne,col)

    def pasOccuper(self, board, newPosition):
       # if self.enemie:
           # self.enemie = False
            #return False
        # verifie si la nouvelle position
        if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[0] > 7 or newPosition[1] > 7:
            return False
        try:
            piece = board[newPosition[0]][newPosition[1]]
            # si la case n'est pas occupé
            if piece == None:
                return True
            # si dans la nouvelle position se trouve une piece de la meme couleur
            elif piece.getColor() == self.color:
                return False
            # si c'est une couleur différente alors c'etait un ennemi
            elif piece.getColor() != self.color:
                #self.enemie = True
                return True
            else:
                return True
        except:
            return False

    def __str__(self):
        return self.color

    def get_color(self):
        pass
    def setMaposition (self,position):
        self.maPosition=position

class Pawn(Piece):
    # position est un couple (1,2) ligne 2 colonne 3,
    # legal est un liste de position
    def __init__(self, position, color):
        self.promo = False
        self.name = "p"
        super().__init__(position, color)
        self.promotion=""
        self.promu = False
        ############# en PASSANT############
        self.sautercase = False
        self.premierMouvement = True

    def setSauterCase(self, bool):
        self.sautercase = bool

    def getSauterCase(self):
        self.sautercase

    def setpremierMouvement(self, bool):
        self.premierMouvement = bool

    def getpremierMouvement(self):
        return self.premierMouvement
    ###################################
    def setPromu(self, bool):
        self.promu = bool
    def getPromu(self):
       return self.promu
    def getMaposition(self):
        return super().getMaPosition()
    # self.color =  color
    # self.position=position
    # retourne un liste de tuple contenant les mouements legals par rapport à la position
    # les pawns au début peuvent bouger de 2 cases mais sinon ne bouge que d'une case et verticlaement
    # peut sauter case ???
    def legalMoves(self, board):
        moves = []
        maPosition = super().getMaPosition()

        if self.promo == False:
            if self.color == "w":
                # si c'est la première fois qu'on le bouge
                if self.premierMouvement:
                    self.premierMouvement = False
                    nouvelle_Position = (maPosition[0] - 2, maPosition[1])
                    # verifie aussi qu'aucun pion n'est devant lui
                    if super().pasOccuper(board, nouvelle_Position):
                        moves.append(nouvelle_Position)
                # si ce n'est pas un premeir mouvement
                nouvelle_Position = (maPosition[0] - 1, maPosition[1])
                if super().pasOccuper(board, nouvelle_Position):
                    moves.append(nouvelle_Position)
            # si c'est un noir
            else:
                if self.premierMouvement:
                    self.premierMouvement = False
                    nouvelle_Position = (maPosition[0] + 2, maPosition[1])
                    if super().pasOccuper(board, nouvelle_Position):
                        moves.append(nouvelle_Position)
                # si ce n'est pas un premeir mouvement
                nouvelle_Position = (maPosition[0] + 1, maPosition[1])
                if super().pasOccuper(board, nouvelle_Position):
                    moves.append(nouvelle_Position)
        diagonale = pionDagonale(board, self)
        for pos in diagonale:
            moves.append(pos)
        ########## PAWN PROMOTION ###########
        if self.promo == True :
            if self.promotion=="rook":
                devant = True
                derriere = True
                gauche = True
                droite = True
                while devant:
                    prochainePos = (maPosition[0] - 1, maPosition[1])
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        devant = False
                        maPosition = super().getMaPosition()

                maPosition = super().getMaPosition()
                while derriere:
                    prochainePos = (maPosition[0] + 1, maPosition[1])
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        derriere = False
                        maPosition = super().getMaPosition()

                maPosition = super().getMaPosition()
                while droite:
                    prochainePos = (maPosition[0], maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        droite = False
                        maPosition = super().getMaPosition()

                maPosition = super().getMaPosition()
                while gauche:
                    prochainePos = (maPosition[0], maPosition[1] - 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        gauche = False
                        maPosition = super().getMaPosition()

            if self.promotion=="knight":
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        if (abs(i) == 1 and abs(j) == 2) or (abs(i) == 2 and abs(j) == 1):
                            nouvellePosition = (maPosition[0] + i, maPosition[1] + j)
                            if super().pasOccuper(board, nouvellePosition):
                                moves.append(nouvellePosition)
            if self.promotion == "bishop":
                gaucheHaut = True
                gaucheBas = True
                droiteHaut = True
                droiteBas = True

                while gaucheHaut:
                    prochainePos = (maPosition[0] - 1, maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        gaucheHaut = False
                        maPosition = super().getMaPosition()

                while gaucheBas:
                    prochainePos = (maPosition[0] + 1, maPosition[1] - 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        gaucheBas = False
                        maPosition = super().getMaPosition()

                while droiteHaut:
                    prochainePos = (maPosition[0] - 1, maPosition[1] - 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        droiteHaut = False
                        maPosition = super().getMaPosition()

                while droiteBas:
                    prochainePos = (maPosition[0] + 1, maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        droiteBas = False
                        maPosition = super().getMaPosition()
            if self.promotion == "queen":
                gaucheHaut = True
                gaucheBas = True
                droiteHaut = True
                droiteBas = True
                devant = True
                derriere = True
                droite = True
                gauche = True

                while gaucheHaut:
                    prochainePos = (maPosition[0] - 1, maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        gaucheHaut = False
                        maPosition = super().getMaPosition()

                while gaucheBas:
                    prochainePos = (maPosition[0] + 1, maPosition[1] - 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        gaucheBas = False
                        maPosition = super().getMaPosition()

                while droiteHaut:
                    prochainePos = (maPosition[0] - 1, maPosition[1] - 1)
                    if self.pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        droiteHaut = False
                        maPosition = super().getMaPosition()

                while droiteBas:
                    prochainePos = (maPosition[0] + 1, maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos
                    else:
                        droiteBas = False
                        maPosition = super().getMaPosition()

                while devant:
                    prochainePos = (maPosition[0] - 1, maPosition[1])
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        devant = False
                        maPosition = super().getMaPosition()

                while derriere:
                    prochainePos = (maPosition[0] + 1, maPosition[1])
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        derriere = False
                        maPosition = super().getMaPosition()

                while droite:
                    prochainePos = (maPosition[0], maPosition[1] + 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        droite = False
                        maPosition = super().getMaPosition()

                while gauche:
                    prochainePos = (maPosition[0], maPosition[1] - 1)
                    if super().pasOccuper(board, prochainePos):
                        moves.append(prochainePos)
                        maPosition = prochainePos

                    else:
                        gauche = False
                        maPosition = super().getMaPosition()
        return moves

    def __str__(self):
        return self.color + self.name

    def getName(self):
        return self.name
    def getPromotion(self):
        return self.promotion
    def setPromotion(self, promotion):
        self.promotion = promotion
    def setPromo(self, promo):
        self.promo = promo
    def unicode(self):
        if self.color == "b" :
            return "\u265F"
        if self.color == "w":
            return "\u2659"
# classe rook : tour

class Rook(Piece):
    # position est (row, col)
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "r"
        self.deplacer = False
    # la tour se deplace soit devant derriere à gauche ou à droite
    def legalMoves(self, board):
        moves = []
        devant = True
        derriere = True
        gauche = True
        droite = True
        maPosition = super().getMaPosition()

        # A chaque déplacement la tour ne peut se diriger que dans une seule
        # direction. C'est-à-dire, soit elle va vers la droite, soit vers la
        # gauche, soit vers le bas ou vers le haut. Elle n’est pas autorisée
        # à sauter par-dessus des autres pièces. Ce qui signifie qu’elle sera bloquée
        # dès qu’une pièce se trouve sur sa trajectoire
        while devant:
            prochainePos = (maPosition[0]-1, maPosition[1])
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                devant = False
                maPosition = super().getMaPosition()

        maPosition = super().getMaPosition()
        while derriere:
            prochainePos = (maPosition[0]+1, maPosition[1])
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                derriere = False
                maPosition=super().getMaPosition()

        maPosition = super().getMaPosition()
        while droite:
            prochainePos = (maPosition[0], maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                droite = False
                maPosition = super().getMaPosition()

        maPosition = super().getMaPosition()
        while gauche:
            prochainePos = (maPosition[0], maPosition[1] - 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                gauche = False
                maPosition = super().getMaPosition()

        return moves

    def __str__(self):
        return self.color + self.name
    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getDeplacer(self):
        return self.deplacer
    def setDeplacer(self,deplacer):
        self.deplacer = deplacer

    def unicode(self):
        if self.color == "b" :
            return "\u265C"
        if self.color == "w":
            return "\u2656"
# classe cavalier  le Cavalier se déplace en sautant. Il n’est donc pas bloqué
# par ses propres pions comme peuvent l’être les Fous ou toutes les autres pièces du jeu d’échecs.
# la position est un couple (ligne,colonne)
class Knight(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "k"

    def legalMoves(self, board):
        moves = []
        maPosition = super().getMaPosition()
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (abs(i) == 1 and abs(j) == 2) or (abs(i) == 2 and abs(j) == 1):
                    nouvellePosition = (maPosition[0] + i, maPosition[1] + j)
                    if super().pasOccuper(board, nouvellePosition):
                        moves.append(nouvellePosition)
        return moves

    def __str__(self):
        return self.color + self.name
    def getName(self):
        return "k"
    def getColor(self):
        return self.color
    def unicode(self):
        if self.color == "b" :
            return "\u265E"
        if self.color == "w":
            return "\u2658"
#  il ne se déplace qu’en diagonale mais a le privilège de se pouvoir
#  se déplacer d’une ou de plusieurs cases, vers l’avant ou l’arrière.
#  A noter qu’il ne peut se déplacer que sur une seule couleur,
#  c'est-à-dire la couleur de sa case initiale.
# le fou ne peut pas sauter sur une autre pièce,


# gérer une ou plusieurs case ?????
class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "b"

    def legalMoves(self, board):
        moves = []
        maPosition = super().getMaPosition()
        gaucheHaut = True
        gaucheBas = True
        droiteHaut = True
        droiteBas = True

        while gaucheHaut:
            prochainePos = (maPosition[0] - 1, maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                gaucheHaut = False
                maPosition = super().getMaPosition()

        while gaucheBas:
            prochainePos = (maPosition[0] + 1, maPosition[1] - 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                gaucheBas = False
                maPosition = super().getMaPosition()

        while droiteHaut:
            prochainePos = (maPosition[0] - 1, maPosition[1] - 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                droiteHaut = False
                maPosition = super().getMaPosition()

        while droiteBas:
            prochainePos = (maPosition[0] + 1, maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                droiteBas = False
                maPosition = super().getMaPosition()
        return moves

    def __str__(self):
        return self.color + self.name
    def getName(self):
        return "b"
    def getColor(self):
        return self.color
    def unicode(self):
        if self.color == "b" :
            return "\u265D"
        if self.color == "w":
            return "\u2657"
# La dame est une autre pièce que les joueurs d’échecs qualifient
# d’artillerie lourde. De toutes les pièces, elle est la plus polyvalente,
# la plus imprévisible et non moins la plus puissante.
# En effet, sa démarche combine astucieusement celles de la tour et du fou.
# Ce qui veut dire qu’elle peut se déplacer aussi bien en ligne droite qu’à la diagonale. Comme la tour et le fou,
# elle peut sauter un nombre illimité de cases (tant que celles-ci sont vides),
# ce qui lui permet d’aller d’un bout de l’échiquier à l’autre et aussi de contrôler les deux couleurs de celui-ci

class Queen(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "Q"

    # position est un couple (ligne, colonne)
    def legalMoves(self, board):
        moves = []
        maPosition = super().getMaPosition()
        gaucheHaut = True
        gaucheBas = True
        droiteHaut = True
        droiteBas = True
        devant = True
        derriere = True
        droite = True
        gauche = True

        while gaucheHaut:
            prochainePos = (maPosition[0] - 1, maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                gaucheHaut = False
                maPosition = super().getMaPosition()

        while gaucheBas:
            prochainePos = (maPosition[0] + 1, maPosition[1] - 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                gaucheBas = False
                maPosition = super().getMaPosition()

        while droiteHaut:
            prochainePos = (maPosition[0] - 1, maPosition[1] - 1)
            if self.pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                droiteHaut = False
                maPosition = super().getMaPosition()

        while droiteBas:
            prochainePos = (maPosition[0] + 1, maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos
            else:
                droiteBas = False
                maPosition = super().getMaPosition()

        while devant:
            prochainePos = (maPosition[0] - 1, maPosition[1])
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                devant = False
                maPosition = super().getMaPosition()

        while derriere:
            prochainePos = (maPosition[0] + 1, maPosition[1])
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                derriere = False
                maPosition = super().getMaPosition()

        while droite:
            prochainePos = (maPosition[0], maPosition[1] + 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                droite = False
                maPosition = super().getMaPosition()

        while gauche:
            prochainePos = (maPosition[0], maPosition[1] - 1)
            if super().pasOccuper(board, prochainePos):
                moves.append(prochainePos)
                maPosition = prochainePos

            else:
                gauche = False
                maPosition = super().getMaPosition()

        return moves

    def __str__(self):
        return super().__str__() + self.name
    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def unicode(self):
        if self.color == "b" :
            return "\u265B"
        if self.color == "w":
            return "\u2655"
# classe pour le roi
# Sur l’échiquier, le roi se déplace comme la dame, sauf qu’il ne
# peut bouger que d’une seule case à la fois. Donc, il peut se déplacer
# vers n’importe quelle case qui l’entoure (avant, arrière, à droite,
# à gauche), mais à condition bien sûr que celle-ci ne soit pas occupé
# par une pièce amie ou une pièce contrôlée par l’ennemi


class King(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.name = "K"
        self.deplacer = False
    def legalMoves(self, board):

        moves = []
        maPosition = super().getMaPosition()
        for ligne in range(-1, 2):
            for col in range(-1, 2):
                new_pos = (maPosition[0] + ligne, maPosition[1] + col)
                if super().pasOccuper(board, new_pos):
                    moves.append(new_pos)

        return moves

    def __str__(self):
        return super().__str__() + self.name
    def getName(self):
        return super().__str__() + self.name
    def getColor(self):
        return self.color
    def getDeplacer(self):
        return self.deplacer
    def setDeplacer(self,deplacer):
        self.deplacer = deplacer
    def unicode(self):
        if self.color == "b" :
            return "\u265A"
        if self.color == "w":
            return "\u2654"
# classe pour le fou
# gs = GameState()
# print(gs)

