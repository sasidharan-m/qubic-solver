from Coach import Coach
from connect4.Connect4Game import Connect4Game as Game1
from connect4.tensorflow.NNet import NNetWrapper as nn1
from qubic.QubicGame import QubicGame as Game2
from qubic.tensorflow.NNet import NNetWrapper as nn2
from utils import *
import sys, getopt

args1 = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 45,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 50,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': '.connect4/temp/',
    'load_model': False,
    'load_folder_file': ('connect4/dev/models/8x100x50','connect4/best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

args2 = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 180,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 200,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': '.qubic/temp/',
    'load_model': False,
    'load_folder_file': ('qubic/dev/models/8x100x50','qubic/best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

def main(argv):
    game_type = ''
    try:
        opts, args = getopt.getopt(argv,"hg:",["help","game="])
    except getopt.GetoptError:
        print('main.py --game <game name> (game name is either connect4 or qubic)')
        sys.exit(2)
    if len(opts) != 1:
        print('main.py --game <game name> (game name is either connect4 or qubic)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py --game <game name> (game name is either connect4 or qubic)')
            sys.exit()
        elif opt in ('-g', '--game'):
            game_type = arg

    if(game_type == 'connect4'):
        print('Training agent for game connect4...')
        g = Game1(6)
        nnet = nn1(g)

        if args1.load_model:
            nnet.load_checkpoint(args1.load_folder_file[0], args1.load_folder_file[1])

        c = Coach(g, nnet, args1)
        if args1.load_model:
            print("Load trainExamples from file")
            c.loadTrainExamples()
        c.learn()
    elif(game_type == 'qubic'):
        print('Training agent for game qubic...')
        g = Game2(4,4,4)
        nnet = nn2(g)

        if args2.load_model:
            nnet.load_checkpoint(args2.load_folder_file[0], args2.load_folder_file[1])

        c = Coach(g, nnet, args2)
        if args2.load_model:
            print("Load trainExamples from file")
            c.loadTrainExamples()
        c.learn()
    else:
        print('Invalid game. Valid games are:')
        print('connect4')
        print('qubic')

if __name__=="__main__":
    main(sys.argv[1:])
