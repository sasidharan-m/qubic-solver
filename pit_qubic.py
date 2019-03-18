import Arena
from MCTS import MCTS
from qubic.QubicGame import QubicGame, display
from qubic.QubicPlayers import *
from qubic.tensorflow.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

import sys, getopt
"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

def pselect(ptype):
    if(ptype == 'random'):
        return 0
    if(ptype == 'heuristic'):
        return 1
    if(ptype == 'minimax'):
        return 2
    if(ptype == 'alphazero'):
        return 3
    if(ptype == 'human'):
        return 4
    print('Invalid player')
    sys.exit(2)

def main(argv):
    game_type = ''
    player_types = ['random', 'heuristic', 'minimax', 'alphazero', 'human']
    p1 = ''
    p2 = ''
    try:
        opts, args = getopt.getopt(argv,"hp:o:",["help","player=","opponent="])
    except getopt.GetoptError:
        print('pit_qubic.py -p <player type> -o <opponent type> (random, heuristic, minimax, alphazero, human)')
        sys.exit(2)
    if len(opts) != 2:
        print('pit_qubic.py -p <player type> -o <opponent type> (random, heuristic, minimax, alphazero, human)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pit_qubic.py -p <player type> -o <opponent type> (random, heuristic, minimax, alphazero, human)')
            sys.exit()
        elif opt in ('-p', '--player'):
            p1 = arg
        elif opt in ('-o', '--opponent'):
            p2 = arg
    if ((p1 not in player_types) or (p2 not in player_types)):
        print('Invalid player types. Valid player types are:')
        print('random')
        print('heuristic')
        print('minimax')
        print('alphazero')
        print('human')
        sys.exit(2)


    args = dotdict({
        'checkpoint': '.qubic/temp/',
        'load_folder_file': ('qubic/dev/models/8x100x50','qubic/best.pth.tar'),
    })
    g = QubicGame(4,4,4)
    p1_ind = pselect(p1)
    p2_ind = pselect(p2)
    print('playing ' + player_types[p1_ind] + ' against ' + player_types[p2_ind] + '...')
    # all players
    rp = RandomPlayer(g).play
    gp = HeuristicQubicPlayer(g).play
    mp = MiniMaxQubicPlayer(g).play
    hp = HumanQubicPlayer(g).play

    # nnet players
    n1 = NNet(g)

    n1.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
    args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
    player_list = [rp, gp, mp, n1p, hp]



    arena = Arena.Arena(player_list[p1_ind], player_list[p2_ind], g, display=display)
    print(arena.playGames(10, verbose=True))

if __name__=="__main__":
    main(sys.argv[1:])
