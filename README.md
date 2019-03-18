# alphazero-solver
Implementation of the AlphaZero algorithm for qubic - (3 Dimensional Tic Tac Toe)
and connect4.

Authors:
Sasidharan Mahalingam (Overall framework integration, modyfing and fixes bugs
  in the alpha zero implementation)
Rafael Espericueta (Implementation of the Simple Heuristic Agent)
Eliana Stefani (Implementation of MiniMax Agent)

Packages Required:
Python - 3.5 or later
Tensorflow - 1.12 or later
(Tensorflow-gpu with a working GPU accelarator recommended)
Atleast 400 GB of free space on disk recommeded to saved the models trained

Instructions to Train an AlphaZero Agent for Connect4:
python main.py --game connect4

Instructions to Train an AlphaZero Agent for Qubic:
python main.py --game qubic

Instructions to run the trained model for connect4:
python pit.py -p <player type> -o <opponent type> (random, heuristic, minimax, alphazero, human)

Instructions to run the trained model for qubic:
python pit_qubic.py -p <player type> -o <opponent type> (random, heuristic, minimax, alphazero, human)

Acknowledgement:  
The framework is based on the implementation of Surag Nair for the game Othello
