from Piece import *
from  chessFunction import *
import time
from datetime import datetime

def jouer(file):
    fichier = open(file, "w")
    pgn = open ("jeu.pgn", "w")
    mouvement= 1
    config = input ("Do you want to load your game yes or not? ")
    affichage =input ("How do you want to display your game in unicode or text? ")
    pgn.write("[Event 'Return Match']\n[Site 'Paris'] \n[Date "+str(datetime.now())+ "]\n[Round '1']\n")
    name = input("What is name of the white player ? ")
    pgn.write("[White  '"+name+"']\n")
    name = input("What is name of the black player ? ")
    pgn.write("[Black  '" + name + "']\n")

    board = [[None, None, None, None, None, None, None, None],  # première rangé pour les noirs bK = black King
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None]  # pour les whites
             ]
    if config == "yes" :
        file = input("Enter the file name : ")
        with open(file) as f :
            for line in f :
                configuration(line, board)
    else :
        # instantiate main black pieces
        board[0][0] = Rook((0, 0), 'b')
        board[0][1] = Knight((0, 1), 'b')
        board[0][2] = Bishop((0, 2), 'b')
        board[0][3] = Queen((0, 3), 'b')
        board[0][4] = King((0, 4), 'b')
        board[0][5] = Bishop((0, 5), 'b')
        board[0][6] = Knight((0, 6), 'b')
        board[0][7] = Rook((0, 7), 'b')
        # instantiate main white pieces
        board[7][0] = Rook((7, 0), 'w')
        board[7][1] = Knight((7, 1), 'w')
        board[7][2] = Bishop((7, 2), 'w')
        board[7][3] = Queen((7, 3), 'w')
        board[7][4] = King((7, 4), 'w')
        board[7][5] = Bishop((7, 5), 'w')
        board[7][6] = Knight((7, 6), 'w')
        board[7][7] = Rook((7, 7), 'w')

    t = input("How much time do you want to give both players (in seconds)? ")
    tempsMax= int(t)
    timeA = 0
    timeB= 0


    for col in range(8):
        board[1][col] = Pawn((1, col), 'b')
        board[6][col] = Pawn((6, col), 'w')


    for col in range(8):
        board[1][col].setpremierMouvement(True)
        board[6][col].setpremierMouvement(True)

    #print(Pawn((4, 0), 'w').legalMoves(board))
    fini = True
    print("Welcome to a game of chess")
    fichier.write("Welcome to a game of chess\n")

    while fini:

        pgn.write(str(mouvement) + ". ")
        s = ""
        ####### WHITE MOVES ##################
        print(afficheBoard(board,affichage))
        fichier.write(afficheBoard(board,affichage)+"\n")
        print("White moves")
        fichier.write("White moves\n")
        start = time.time()
        p = input("Indicate piece position : ")
        if p== "R":
            resign("w",fichier)
            pgn.write("0-1")
            break
        if p =="Draw":
            draw = input("Does the black player agree ? ")
            if draw == "yes":
                drawing(fichier)
                pgn.write("1/2-1/2")
                break
            else :
                continue
        timeA += time.time() - start
        if timeA>=tempsMax:
            timesUp("Black", fichier)
            print(afficheBoard(board, affichage))
            fichier.write(afficheBoard(board, affichage) + "\n")
            pgn.write("0-1")
            break
        fichier.write("Indicate piece position : "+p+"\n")
        try:
            position = change_stringToPosition(p)
        except EchecExeption:
            print ("**********Errror position**********")
        pieceDeplacee = board[position[0]][position[1]]

        ####  petit roque castling#########
        start = time.time()
        d = input("Indicate piece destination : ")
        timeA += time.time() - start
        if timeA>=tempsMax:
            timesUp("Black", fichier)
            print(afficheBoard(board, affichage))
            fichier.write(afficheBoard(board, affichage) + "\n")
            pgn.write("0-1")
            break
        fichier.write("Indicate piece destination : "+d+"\n")

        if len(d)==2 :
            destination = change_stringToPosition(d)
            try :
                moves = board[position[0]][position[1]].legalMoves(board)
            except EchecExeption:
                print("**********Errror position**********")
            destEnPassant = ()
            posPionPrisEnPassant = ()

            # si la dstination est dans le legalMoves de la piece à la position position
            if destination in moves:
                pieceTrouvée = board[destination[0]][destination[1]]
                board[destination[0]][destination[1]] = board[position[0]][position[1]]
                board[destination[0]][destination[1]].setMaposition(destination)
                board[position[0]][position[1]] = None
            else:
                while (destination in moves) == False:
                    start = time.time()
                    print("Forbidden movement.")
                    fichier.write("Forbidden movement."+"\n")
                    d = input("Indicate piece destination : ")
                    timeA += time.time() - start
                    fichier.write("Indicate piece destination : "+d+"\n")
                    try :
                        destination = change_stringToPosition(d)
                    except EchecExeption:
                        print("**********Errror position**********")
                    if timeA >= tempsMax:
                        timesUp("Black", fichier)
                        print(afficheBoard(board, affichage))
                        fichier.write(afficheBoard(board, affichage) + "\n")
                        pgn.write("0-1")
                        break
                if timeA >= tempsMax:
                    break
                pieceTrouvée = board[destination[0]][destination[1]]
                board[destination[0]][destination[1]] = board[position[0]][position[1]]
                board[destination[0]][destination[1]].setMaposition(destination)
            if detectEchec(board, "b"):
                print ("Attention !!! Black king is in check")
                fichier.write("Attention !!! Black king is in check\n")
            if pieceTrouvée==None :
                s+=stringforPgn(pieceDeplacee) + d
            else :
                s += stringforPgn(pieceDeplacee)+"x"+ d
            board[position[0]][position[1]] = None

            if isinstance(board[destination[0]][destination[1]], King) or isinstance(board[destination[0]][destination[1]], Rook):
                board[destination[0]][destination[1]].setDeplacer(True)
            board[position[0]][position[1]] = None

            if position[1] == destination[1]-2 and isinstance(board[destination[0]][destination[1]],Pawn)==True:
                board[destination[0]][destination[1]].setSauterCase(True)

            if (pieceTrouvée!=None and pieceTrouvée.getName()=="bK") or timeB>= 600:
                print("White won !!")
                fichier.write("White won !!\n")
                board[position[0]][position[1]] = None
                print(afficheBoard(board,affichage))
                fichier.write(afficheBoard(board,affichage)+"\n")
                pgn.write(" 1-0")
                break
                ############## PAWN PROMOTiON#########@#@@
            if board[destination[0]][destination[1]] !=None and board[destination[0]][destination[1]].getName() == "p" and destination[0] == 0:
                pion = board[destination[0]][destination[1]]
                if pion.getPromu()==False :
                    pion.setPromu(True)
                    print("Pawn promotion !!")
                    pion.setPromo(True)
                    fichier.write("Pawn promotion !!\n")
                    promo = input("Which promotion do you choose? a) rook b) queen c) bishop d) knight ")
                    fichier.write("Which promotion do you choose? a) rook b) queen c) bishop d) knight " + promo)
                    j = ""
                    if promo == "a":
                        pion.setPromotion("rook")
                        j = "rook"
                        s+"=R"
                    if promo == "b":
                        pion.setPromotion("queen")
                        s+="=Q"
                        j = "queen"
                    if promo == "c":
                        pion.setPromotion("bishop")
                        s+="=B"
                        j = "bishop"
                    if promo == "d":
                        pion.setPromotion("knight")
                        s+="=N"
                        j = "knight"
                    print("Your pawn is now a " + pion.getPromotion())
                    fichier.write("Your pawn is now a " + pion.getPromotion() + "\n")


        elif d =="Petitroque" :
            if board[7][4].getName() == "wK" and isinstance(board[7][7],Rook)== True and verifPetitRoque(board, "w") == True and board[7][4].getDeplacer()==False and board[7][7].getDeplacer()==False :
                print(str(board[7][7]))
                # change position roi
                board[7][6] = King((7, 6), 'w')
                board[7][6].setDeplacer = True
                board[7][4] = None
                # change position du roque (tour)
                board[7][5] = Rook((7, 5), 'w')
                board[7][5].setDeplacer = True
                board[7][7] = None
                s+="O-O"

        elif d=="Grandroque":
            if board[7][4].getName() == "wK"  and isinstance(board[7][0],Rook)== True  and verifGrandroque(board, "w") == True and board[7][4].getDeplacer()==False and board[7][0].getDeplacer()==False:
                    board[7][2] = King((7, 2), 'w')
                    board[7][2].setDeplacer = True
                    board[7][4] = None
                    # change position du roque (tour)
                    board[7][3] = Rook((7, 3), 'w')
                    board[7][3].setDeplacer = True
                    board[7][0] = None
                    s+="O-O-0"

        pgn.write(s + " ")
    #if dangerRoiNoir(board):
       # fini = False
        #print("White win")
        #break


        ####### BLACK  MOVES ##################
        s=" "
        startB = time.time()
        print(afficheBoard(board,affichage))
        fichier.write(afficheBoard(board,affichage)+"\n")
        print("Black moves")
        fichier.write("Black moves\n")
        p = input("Indicate piece position : ")
        if p == "R":
            resign("b", fichier)
            pgn.write("1-0")
            break
        if p =="Draw":
            draw = input("Does the white player agree ? ")
            if draw == "yes":
                drawing(fichier)
                pgn.write("1/2-1/2")
                break
            else :
                continue
        timeB += time.time() - startB
        if timeB >= tempsMax:
            timesUp("White", fichier)
            print(afficheBoard(board, affichage))
            fichier.write(afficheBoard(board, affichage) + "\n")
            pgn.write(" 1-0")
            break
        fichier.write("Indicate piece position : " + p + "\n")
        position = change_stringToPosition(p)
        pieceDeplacee = board[position[0]][position[1]]
        startB = time.time()
        d = input("Indicate piece destination : ")
        timeB += time.time() - startB
        if timeB >= tempsMax:
            timesUp("White", fichier)
            print(afficheBoard(board, affichage))
            fichier.write(afficheBoard(board, affichage) + "\n")
            pgn.write(" 1-0")
            break
        fichier.write("Indicate piece destination : " + d + "\n")


        if len(d)==2:
            try :
                destination = change_stringToPosition(d)
            except EchecExeption:
                print("**********Errror position**********")
            moves = board[position[0]][position[1]].legalMoves(board)
            posPionPrisEnPassant =()
            destEnPassant=()
            ########## EN PASSANT###################
            if board[position[0]][position[1]].getName() =="p" and board[position[0]][position[1]].getColor == "b":
                pion = board[position[0]][position[1]]
                if enPassantGauche(board, pion) == True:
                    posPionPrisEnPassant = (position[0] , position[1]- 1)
                    destEnPassant = (position[0] - 1, position[0] - 1)
                if enPassantDroite(board, pion) == True:
                    posPionPrisEnPassant = (position[0], position[1] + 1)
                    destEnPassant = (position[0] -1, position[0] + 1)
            if posPionPrisEnPassant != () and board[posPionPrisEnPassant[0]][posPionPrisEnPassant[1]].getSauterCase() == True:
                moves.append(destEnPassant)
                board[posPionPrisEnPassant[0]][posPionPrisEnPassant[1]].setSauterCase(False)
            ####################################################
            # si la dstination est dans le legalMoves de la piece à la position position
            if destination in moves :
                pieceTrouvée = board[destination[0]][destination[1]]
                board[destination[0]][destination[1]] = board[position[0]][position[1]]
                board[destination[0]][destination[1]].setMaposition(destination)
                board[position[0]][position[1]] = None
                timeB += time.time() - startB
            else:
                while (destination in moves) == False:
                    print("Forbidden movement.")
                    fichier.write("Forbidden movement." + "\n")
                    startB = time.time()
                    d = input("Indicate piece destination : ")
                    timeB += time.time() - startB
                    fichier.write("Indicate piece destination : " + d + "\n")
                    destination = change_stringToPosition(d)
                    if timeB >= tempsMax:
                        timesUp("White", fichier)
                        print(afficheBoard(board, affichage))
                        fichier.write(afficheBoard(board, affichage) + "\n")
                        pgn.write(" 1-0")
                        break
                if timeB >= tempsMax:
                    break
                pieceDeplacee = board[position[0]][position[1]]
                pieceTrouvée = board[destination[0]][destination[1]]
                board[destination[0]][destination[1]] = board[position[0]][position[1]]
                board[destination[0]][destination[1]].setMaposition(destination)

            if pieceTrouvée==None :
                s+=stringforPgn(pieceDeplacee) + d
            else :
                s += stringforPgn(pieceDeplacee)+"x"+ d
            if detectEchec(board, "w"):
                print ("Attention !!! White king is in check")
                fichier.write("Attention !!! White king is in check\n")
            board[position[0]][position[1]] = None
            timeB += time.time() - startB
            if isinstance(board[destination[0]][destination[1]], King) or isinstance(board[destination[0]][destination[1]], Rook):
                board[destination[0]][destination[1]].setDeplacer(True)
            board[position[0]][position[1]] = None

                ####EN PASSANT #############
            if position[1] == destination[1] +2 and isinstance(board[destination[0]][destination[1]], Pawn) == True:
                board[destination[0]][destination[1]].setSauterCase(True)

            if (pieceTrouvée != None and pieceTrouvée.getName()=="wK") or timeA>600:
                print("Black won !!")
                fichier.write("Black won !!")
                board[position[0]][position[1]] = None
                print(afficheBoard(board, affichage))
                pgn.write("0-1")
                fichier.write(afficheBoard(board, affichage) + "\n")
                break
            ############## PAWN PROMOTiON#########@#@@
            if board[destination[0]][destination[1]].getName()=="p" and destination[0] == 7:

                pion = board[destination[0]][destination[1]]
                if pion.getPromu()==False :
                    pion.setPromu(True)
                    print("Pawn promotion !!")
                    pion.setPromo(True)
                    fichier.write("Pawn promotion !!\n")
                    promo = input("Which promotion do you choose? a) rook b) queen c) bishop d) knight ")
                    fichier.write("Which promotion do you choose? a) rook b) queen c) bishop d) knight "+promo)
                    j=""
                    if promo=="a":
                        pion.setPromotion("rook")
                        s+"=R"
                        j="rook"
                    if promo == "b":
                        pion.setPromotion("queen")
                        s+="=Q"
                        j="queen"
                    if promo == "c":
                        pion.setPromotion("bishop")
                        s+="=B"
                        j="bishop"
                    if promo == "d":
                        pion.setPromotion("knight")
                        s+="=N"
                        j="knight"
                    print("Your pawn is now a "+pion.getPromotion())
                    fichier.write("Your pawn is now a "+pion.getPromotion()+"\n")

        if d == "Petitroque":
            if board[0][4].getName() == "bK" and isinstance(board[0][7], Rook) == True and verifPetitRoque(board,
                                                                                                           "b") == True:
                # change position roi
                board[0][6] = King((0, 6), 'b')
                board[0][6].setDeplacer = True
                board[0][4] = None
                # change position du roque (tour)
                board[0][5] = Rook((0, 5), 'b')
                board[0][5].setDeplacer = True
                board[0][7] = None
                s+="O-O"

        elif d == "Grandroque":
            if board[0][4].getName() == "bK" and isinstance(board[0][0], Rook) == True and verifGrandroque(board,
                                                                                                           "b") == True:
                # change position roi
                board[0][2] = King((0, 2), 'b')
                board[0][2].setDeplacer(True)
                board[0][4] = None
                # change position du roque (tour)
                board[0][3] = Rook((0, 3), 'b')
                board[0][3].setDeplacer(True)
                board[0][0] = None
                s+="O-O-0"

        pgn.write(s+" ")
        mouvement+=1

    fichier.close()
    pgn.close()



# pawn promotion qaund un pion arrive à l'autre bout du plateau il devien une rein
jouer("echec.txt")


