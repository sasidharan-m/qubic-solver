import Arena
from MCTS import MCTS
from qubic.QubicGame import QubicGame, display
from qubic.QubicPlayers import *
from qubic.tensorflow.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
args = dotdict({
    'checkpoint': '.qubic/temp/',
    'load_folder_file': ('qubic/dev/models/8x100x50','qubic/best.pth.tar'),
})
g = QubicGame(4,4,4)

# all players
rp = RandomPlayer(g).play
#gp = OneStepLookaheadConnect4Player(g).play
mp = MiniMaxQubicPlayer(g).play
#hp = HumanConnect4Player(g).play

# nnet players
n1 = NNet(g)
#n1.load_checkpoint('./pretrained_models/othello/pytorch/','6x100x25_best.pth.tar')
n1.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


#n2 = NNet(g)
#n2.load_checkpoint('/dev/8x50x25/','best.pth.tar')
#args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
#mcts2 = MCTS(g, n2, args2)
#n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena.Arena(n1p, mp, g, display=display)
print(arena.playGames(10, verbose=True))
