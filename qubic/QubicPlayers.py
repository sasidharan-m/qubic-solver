import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        d = np.random.randint(4)
        r = np.random.randint(4)
        c = np.random.randint(4)

        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanConnect4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        print('\nMoves:', [i for (i, valid) in enumerate(valid_moves) if valid])

        while True:
            move = int(input())
            if valid_moves[move]: break
            else: print('Invalid move')
        return move

class MiniMaxQubicPlayer():
    def __init__(self, game):
        self.game = game

    def update_board(self, board, move, player_num):
        if board[move] == 0:
            board[move] = player_num
            return board

        else:
            print("Player: "+ str(player_num))
            print("Tried to move to location " + str(move))
            print("Which is occupied by player " + str(board[move]))
            raise Exception("CANNOT MOVE THERE!!! ")

    def utility_fcn(self, board, player):

        def returnStreaks(board):
            streak = np.zeros((76, 4), dtype=np.uint8)

            # ULTRA DIAGONALS in 3D

            # From front, top left
            streak[0] = [board[0, 0, 0],
                         board[1, 1, 1],
                         board[2, 2, 2],
                         board[3, 3, 3]]

            # From back, top left
            streak[1] = [board[3, 0, 0],
                         board[2, 1, 1],
                         board[1, 2, 2],
                         board[0, 3, 3]]

            # From front, bottom left
            streak[2] = [board[0, 3, 0],
                         board[1, 2, 1],
                         board[2, 1, 2],
                         board[3, 0, 3]]

            # From back, bottom left
            streak[3] = [board[3, 3, 0],
                         board[2, 2, 1],
                         board[1, 1, 2],
                         board[0, 0, 3]]

            # CHECK ANTI/DIAGONALS in 2D
            for cut in range(4):
                # DIAGONALS by LAYER
                streak[cut + 4] = [board[cut, 0, 0],
                                   board[cut, 1, 1],
                                   board[cut, 2, 2],
                                   board[cut, 3, 3]]

                # ANTI DIAGONALS by LAYER
                streak[cut + 8] = [board[cut, 0, 3],
                                   board[cut, 1, 2],
                                   board[cut, 2, 1],
                                   board[cut, 3, 0]]

                # DIAGONALS by ROW
                streak[cut + 12] = [board[0, cut, 0],
                                    board[1, cut, 1],
                                    board[2, cut, 2],
                                    board[3, cut, 3]]

                # ANTI DIAGONALS by ROW
                streak[cut + 16] = [board[0, cut, 3],
                                    board[1, cut, 2],
                                    board[2, cut, 1],
                                    board[3, cut, 0]]

                # DIAGONALS by COL
                streak[cut + 20] = [board[0, 0, cut],
                                    board[1, 1, cut],
                                    board[2, 2, cut],
                                    board[3, 3, cut]]

                # ANTI DIAGONALS by COL
                streak[cut + 24] = [board[0, 3, cut],
                                    board[1, 2, cut],
                                    board[2, 1, cut],
                                    board[3, 0, cut]]

            index = 28
            # STACK POINTS
            for row in range(4):
                for col in range(4):
                    streak[index] = board[0:4, row, col]
                    index = index + 1
            # ROW POINTS
            for stack in range(4):
                for row in range(4):
                    streak[index] = board[stack, row, 0:4]
                    index = index + 1
            # COL POINTS
            for stack in range(4):
                for col in range(4):
                    streak[index] = board[stack, 0:4, col]
                    index = index + 1

            return streak

        # CHECK POINTS, on each row slice (3*16 in 1d, 24 in 2d, 4 in 4d)
        def value(self, streak, player):

            points = 0
            for i in range(len(streak)):

                # if i==44:
                #     print streak[i]
                #     print("Player: "+str(player)+" Opponent:"+str(((player % 2) + 1))+"\n")


                if ((player % 2) + 1) in streak[i]:  # No points if opponent is present
                    # print("\t\tOpponent Present")
                    continue
                else:
                    numTokensInStreak = np.equal(streak[i], player)
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        points = inf
                        # print("\t\tWIN!")
                        return points
                    else:
                        points = points + streakScore ** 3
                        # print("\t\tScore: " + str(streakScore ** 2))
            return points

        opponent = (player % 2) + 1
        streak = returnStreaks(board)

        utilityPlayer   = value(streak, player)
        utilityOpponent = value(streak, opponent)

        utility = utilityPlayer - utilityOpponent

        # print("Utility Player:   " +str(player)+": "+str(utilityPlayer))
        # print("Utility Opponent: " +str(opponent)+": "+str(utilityOpponent))
        # print("\nOverall Utility for player " +str(player)+": "+str(utility)+"\n\n")

        return utility

    def MaxValue(self, playerNumber, board4max, alpha, beta, depth2go4max):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4max, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4max == 0) or (abs(utility) == inf):
            return [utility, -1]


        value = -inf
        action2return = (-1,-1,-1)

        for layer in range(4):
            for row in range(4):
                for col in range(4):



                    if board4max[layer, row, col] != 0:            # Check if move is valid
                        continue

                    action = (layer, row, col)

                    if(action2return == (-1,-1,-1)):
                        action2return = action

                    child_board = board4max.copy()
                    child_board = self.update_board(child_board, action, playerNumber)




                    min_child_value = self.MinValue(playerNumber, child_board, alpha, beta, depth2go4max - 1)[0]


                    # if depth2go4max == 2:
                    #     print("Move: " + str(action) + "  Value: " + str(min_child_value))

                    if (min_child_value > value):
                        value = min_child_value
                        action2return = action

                    if value >= beta:
                        return [value, action2return]
                    alpha = max(alpha, value)


        return [value, action2return]

    def MinValue(self, playerNumber, board4min, alpha, beta, depth2go4min):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4min, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4min == 0) or (abs(utility) == inf):
            return [utility, -1]

        opponent = (playerNumber % 2) + 1
        value = inf
        # action2return = (-1,-1,-1)


        for layer in range(4):
            for row in range(4):
                for col in range(4):

                    if board4min[layer, row, col] != 0:  # Check if move is valid
                        continue

                    action = (layer, row, col)

                    # if (action == (-1, -1, -1)):
                    #     action2return = action

                    child_board = board4min.copy()
                    child_board = self.update_board(child_board, action, opponent)



                    max_child_value = self.MaxValue(playerNumber, child_board, alpha, beta, depth2go4min - 1)[0]


                    if max_child_value < value:
                        value = max_child_value


                    if value <= alpha:
                        return [value, -1]
                    beta = max(beta, value)


        return [value, -1]


    def play(self, board):
        self.depth2go = 3
        self.player = 1
        tmp_board = np.copy(board)
        for i in range(self.rows):
            for j in range(self.cols):
                if(tmp_board[i][j] == -1):
                    tmp_board[i][j] = 2
        [reward, action] = self.MaxValue(player, board, -inf, inf, depth2go)
        if action == -1:
            raise ValueError ('Invalid move happened while playing. Aborting...')
        return (16*action[0] + 4*action[1] + action[2])
