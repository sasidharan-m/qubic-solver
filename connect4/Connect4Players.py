import numpy as np
from numpy import inf
import math

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
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


class OneStepLookaheadConnect4Player():
    """Simple player who always takes a win if presented, or blocks a loss if obvious, otherwise is random."""
    def __init__(self, game, verbose=True):
        self.game = game
        self.player_num = 1
        self.verbose = verbose

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, self.player_num)
        win_move_set = set()
        fallback_move_set = set()
        stop_loss_move_set = set()
        for move, valid in enumerate(valid_moves):
            if not valid: continue
            if self.player_num == self.game.getGameEnded(*self.game.getNextState(board, self.player_num, move)):
                win_move_set.add(move)
            if -self.player_num == self.game.getGameEnded(*self.game.getNextState(board, -self.player_num, move)):
                stop_loss_move_set.add(move)
            else:
                fallback_move_set.add(move)

        if len(win_move_set) > 0:
            ret_move = np.random.choice(list(win_move_set))
            if self.verbose: print('Playing winning action %s from %s' % (ret_move, win_move_set))
        elif len(stop_loss_move_set) > 0:
            ret_move = np.random.choice(list(stop_loss_move_set))
            if self.verbose: print('Playing loss stopping action %s from %s' % (ret_move, stop_loss_move_set))
        elif len(fallback_move_set) > 0:
            ret_move = np.random.choice(list(fallback_move_set))
            if self.verbose: print('Playing random action %s from %s' % (ret_move, fallback_move_set))
        else:
            raise Exception('No valid moves remaining: %s' % game.stringRepresentation(board))

        return ret_move

class MiniMaxConnect4Player():
    """Minimax player for connect4"""
    def __init__(self, game, verbose=True):
        self.game = game
        self.player_num = 1
        self.verbose = verbose

    def update_board(self, board, move, player_num):
        if 0 in board[:,move]:
            update_row = -1
            for row in range(1, board.shape[0]):
                update_row = -1
                if board[row, move] > 0 and board[row-1, move] == 0:
                    update_row = row-1
                elif row==board.shape[0]-1 and board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    board[update_row, move] = player_num
                    break
        else:
            print("COULDN'T TEST BOARD UPDATE!!!")

        return board

    def utility_fcn(self, board, player):

        # CHECK VERTICAL POINTS
        def valueVertical(board, player):
            vPoints = 0

            for row in range(self.rows - 3):
                for col in range(self.cols):

                    # Look at potential streak of four
                    streak = board[row:(row + 4), col]
                    if ((player % 2) + 1) in streak:
                        # print("Streak: " + str(streak))
                        continue

                    # How many tokens placed in that streak?
                    numTokensInStreak = np.equal(streak, player)

                    # Score = square of number of tokens in possible streak
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        vPoints = inf
                        return vPoints
                    vPoints = vPoints + streakScore ** 2

                    # print("Streak: " + str(streak) + "   NumTokInStreak: " + str(numTokensInStreak)+ "   Score: " + str(streakScore))
            return vPoints

        # CHECK HORIZONTAL POINTS
        def valueHorizontal(board, player):
            hPoints = 0

            for col in range(self.cols - 3):
                for row in range(self.rows):

                    # Look at potential streak of four
                    streak = board[row, col:(col + 4)]
                    if ((player % 2) + 1) in streak:
                        # print("Streak: " + str(streak))
                        continue

                    # How many tokens placed in that streak?
                    numTokensInStreak = np.equal(streak, player)

                    # Score = square of number of tokens in possible streak
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        hPoints = inf
                        return hPoints
                    hPoints = hPoints + streakScore ** 2

                    # print("Streak: " + str(streak) + "   NumTokInStreak: " + str(numTokensInStreak)+ "   Score: " + str(streakScore))
            return hPoints

        # CHECK DIAGONAL \ (Negative slope)
        def valueDiagonal(board, player):
            dPoints = 0

            for row in range(self.rows - 3):
                for col in range(self.cols - 3):

                    # Look at potential streak of four
                    streak = [board[row, col],
                              board[row + 1, col + 1],
                              board[row + 2, col + 2],
                              board[row + 3, col + 3]]
                    if ((player % 2) + 1) in streak:
                        # print("Streak: " + str(streak))
                        continue

                    # How many tokens placed in that streak?
                    numTokensInStreak = np.equal(streak, player)

                    # Score = square of number of tokens in possible streak
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        dPoints = inf
                        return dPoints
                    dPoints = dPoints + streakScore ** 2

                    # print("Streak: " + str(streak) + "   NumTokInStreak: " + str(numTokensInStreak)+ "   Score: " + str(streakScore))
            return dPoints

        # CHECK ANTI-DIAGONAL / (Postive Slope)
        def valueAntiDiag(board, player):
            aPoints = 0

            for row in range(3, self.rows):
                for col in range(self.cols - 3):

                    # Look at potential streak of four
                    streak = [board[row, col],
                              board[row - 1, col + 1],
                              board[row - 2, col + 2],
                              board[row - 3, col + 3]]
                    if ((player % 2) + 1) in streak:
                        # print("Streak: " + str(streak))
                        continue

                    # How many tokens placed in that streak?
                    numTokensInStreak = np.equal(streak, player)

                    # Score = square of number of tokens in possible streak
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        aPoints = inf
                        return aPoints
                    aPoints = aPoints + streakScore ** 2

                    # print("Streak: " + str(streak) + "   NumTokInStreak: " + str(numTokensInStreak)+ "   Score: " + str(streakScore))
            return aPoints



        #global self.rows, self.cols
        opponent = (player % 2) + 1
        #print(board)

        utilityPlayer = valueVertical(board, player) + \
                        valueHorizontal(board, player) + \
                        valueDiagonal(board, player) + \
                        valueAntiDiag(board, player)

        utilityOpponent = valueVertical(board, opponent) + \
                          valueHorizontal(board, opponent) + \
                          valueDiagonal(board, opponent) + \
                          valueAntiDiag(board, opponent)

        utility = utilityPlayer - utilityOpponent
        return utility


    def MaxValue(self, playerNumber, board4max, alpha, beta, depth2go4max):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4max, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4max == 0) or (abs(utility) == inf):
            return [utility, -1]

        value = -inf
        action2return = -1
        valueEachActnMax = [0, 0, 0, 0, 0, 0, 0]

        for action in range(7):  # Cycle through the 7 columns
            if 0 not in board4max[:, action]:  # Check if move is valid
                continue

            if(action2return==-1):
                action2return = action

            child_board = board4max.copy()
            child_board = self.update_board(child_board, action, playerNumber)

            # print("\nMax. for P" + str(player) + "  Move: " + str(action) + "  Depth " + str(depth2go))
            # print(child_board)
            # print("\n")

            if(depth2go4max == 4):
                print("               Player 1 action is " + str(action) + "\n")



            min_child_value = self.MinValue(playerNumber, child_board, alpha, beta, depth2go4max - 1)[0]


            if((action == 4 or 3) and depth2go4max == 4):
                print("              Action "+str(action)+"'s min value: " + str(min_child_value) + "\n\n")


            valueEachActnMax[action] = min_child_value

            if(action == 4 and depth2go4max == 4):
                print("ACTION IS 4!!!")
                print(child_board)
                print("\n")

            # 'value = max(value,min_child_value)' AND record the action
            if (min_child_value > value):
                value = min_child_value
                action2return = action

            if value >= beta:
                return [value, action]
            alpha = max(alpha, value)

        if depth2go4max == 4:
            print("High Level sees: \n")
            print(valueEachActnMax)

        return [value, action2return]


    def MinValue(self, playerNumber, board4min, alpha, beta, depth2go4min):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4min, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4min == 0) or (abs(utility) == inf):
            return [utility, -1]

        opponent = (playerNumber % 2) + 1
        value = inf
        action2return = -1
        valueEachActnMin = [0, 0, 0, 0, 0, 0, 0]



        for action in range(self.cols):  # Cycle through the 7 columns
            if 0 not in board4min[:, action]:  # Check if move is valid
                continue

            child_board = board4min.copy()
            child_board = self.update_board(child_board, action, opponent)

            # print("Min for P" + str(opponent) + " Action: " + str(action) + "  Depth " + str(depth2go))
            # print(child_board)
            # print("\n")



            max_child_value = self.MaxValue(playerNumber, child_board, alpha, beta, depth2go4min - 1)[0]
            valueEachActnMin[action] = max_child_value

            #         print("P" + str(opponent) + " Action: " + str(action) + "   Value: " + str(max_child_value) + "  Depth " + str(depth2go))

            if (depth2go4min == 3) and (child_board[1,4]==1):
                print("Child of P2, Action" + str(action) + "  Max value " + str(max_child_value) )
                print(child_board)
                print("\n")

            # value = min(value, max_child_value)
            if max_child_value <= value:
                value = max_child_value
                action2return = action

            if value <= alpha:
                return [value, action]
            beta = max(beta, value)

        # if depth2go4min == 2:
            # print(valueEachActnMin)
        return [value, action2return]


    def play(self, board):
        self.rows = len(board)
        self.cols = len(board[0])
        self.depth2go = 3
        self.player = 1
        tmp_board = np.copy(board)
        for i in range(self.rows):
            for j in range(self.cols):
                if(tmp_board[i][j] == -1):
                    tmp_board[i][j] = 2
        ret_move = self.MaxValue(self.player, tmp_board, - math.inf, math.inf, self.depth2go)[1]
        return ret_move
