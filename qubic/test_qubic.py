"""
To run tests:
pytest-3 qubic
"""

from collections import namedtuple
import textwrap
import numpy as np

from QubicGame import QubicGame

# Tuple of (Board, Player, Game) to simplify testing.
BPGTuple = namedtuple('BPGTuple', 'board player game')

def init_board_from_moves(moves,depth=None, height=None, width=None):
    """Returns a BPGTuple based on series of specified moved."""
    game = QubicGame(depth=depth, height=height, width=width)
    board, player = game.getInitBoard(), 1
    for move in moves:
        board, player = game.getNextState(board, player, move)
    return BPGTuple(board, player, game)


def init_board_from_array(board, player):
    """Returns a BPGTuple based on series of specified moved."""
    game = QubicGame(depth=len(board[0]), height=len(board[1]), width=len(board[2]))
    return BPGTuple(board, player, game)


def test_simple_moves():
    board, player, game = init_board_from_moves([4, 5, 23, 3, 0, 6, 63, 45])
    expected = textwrap.dedent("""\
        [[[ 1.  0.  0. -1.]
          [ 1. -1. -1.  0.]
          [ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]]

         [[ 0.  0.  0.  0.]
          [ 0.  0.  0.  1.]
          [ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]]

         [[ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]
          [ 0. -1.  0.  0.]]

         [[ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]
          [ 0.  0.  0.  0.]
          [ 0.  0.  0.  1.]]]""")
    assert expected == game.stringRepresentation(board)


def check_cube_to_list_conversion():
    """Checks if the cube to list conversion works properly"""
    board, player, game = init_board_from_moves([4, 5, 23, 3, 0, 6, 63, 45])
    ref_list = [1.0, 0.0, 0.0,-1.0,
                1.0,-1.0,-1.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0,-1.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0]
    conv_list = game.convertCubeToList(board)
    assert ref_list == conv_list

def check_list_to_cube_conversion():
    """Check if the list to cube conversion works properly"""
    board, player, game = init_board_from_moves([4, 5, 23, 3, 0, 6, 63, 45])
    ref_list = [1.0, 0.0, 0.0,-1.0,
                1.0,-1.0,-1.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0,-1.0, 0.0, 0.0,

                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0]
    conv_cube = game.convertListToCube(ref_list)
    uq = np.unique(conv_cube == board)
    assert uq.size == 1 and uq[0] == True

def test_overfull_cube():
    moves = []
    for m in range(64):
        moves.append(m)
    # Fill to max capacity is ok
    init_board_from_moves(moves, depth=4, height=4, width=4)

    # Check overfilling causes an error.
    try:
        init_board_from_moves(moves + [63], depth=4, height=4, width=4)
        assert False, "Expected error when overfilling column"
    except ValueError:
        pass  # Expected.


def test_get_valid_moves():
    """Tests vector of valid move is correct."""
    move_valid_pairs = [
        ([], [True] * 64),
        ([0, 1, 2, 3, 4, 5, 6], (([False] * 7) + [True] * (64 - 7))),
        ([1, 2, 3, 4, 5], ([True] + [False] * 5 + [True] * (64 - 6))),
        ([0, 1, 2, 3, 4, 5, 6, 25, 63], ([False] * 7 + [True] * (25-7) + [False] + [True] * (63-26) + [False])),
        #([0, 1, 2] * 3 + [3, 4, 5, 6] * 6, [True] * 3 + [False] * 4),
    ]

    for moves, expected_valid in move_valid_pairs:
        board, player, game = init_board_from_moves(moves, depth=4, height=4, width=4)
        assert (np.array(expected_valid) == game.getValidMoves(board, player)).all()

def get_ref(cube):
    """Gets the 8 reflection symmetries of a nd numpy array"""
    L = []
    L.append(cube[:,:,:])
    L.append(cube[:,:,::-1])
    L.append(cube[:,::-1,:])
    L.append(cube[::-1,:,:])
    L.append(cube[:,::-1,::-1])
    L.append(cube[::-1,:,::-1])
    L.append(cube[::-1,::-1,:])
    L.append(cube[::-1,::-1,::-1])
    return L

def calc_symmetries(cube):
    """Calculates all 48 possible symmetries of a nd numpy array"""
    L = []
    L += get_ref(cube)
    L += get_ref(np.transpose(cube, (0,2,1)))
    L += get_ref(np.transpose(cube, (2,1,0)))
    L += get_ref(np.transpose(cube, (1,0,2)))
    L += get_ref(np.transpose(cube, (2,0,1)))
    L += get_ref(np.transpose(cube, (1,2,0)))
    return L

def convert_cube_into_list(cube):
    l = []
    for i in range(cube.shape[0]):
        for j in range(cube.shape[1]):
            for k in range(cube.shape[2]):
                l.append(cube[i][j][k])
    return l


def test_symmetries():
    """Tests symetric board are produced."""
    board, player, game = init_board_from_moves([0, 1, 45, 6])
    pi_cube = np.array(range(64)).reshape(4,4,4)
    pi = game.convertCubeToList(pi_cube)
    sims = game.getSymmetries(board, pi)
    ref_sims = calc_symmetries(board)
    tmp_pis = calc_symmetries(pi_cube)
    ref_pis = []
    for c in tmp_pis:
        t = game.convertCubeToList(c)
        ref_pis.append(t)
    del_inds = []
    for i in range(len(sims)):
        flag = False
        m = sims[i][0]
        for j in range(len(ref_sims)):
            n = ref_sims[j]
            if(np.array_equal(m,n)):
                #del_inds.append(j)
                del ref_sims[j]
                flag = True
                break
        assert flag, "Cube symmetries not correct"
    #for ind in del_inds:
    #    del ref_sims[ind]
    assert len(ref_sims) == 1 and np.unique(ref_sims == board).size == 1
    del_inds = []
    for i in range(len(sims)):
        flag = False
        m = sims[i][1]
        for j in range(len(ref_pis)):
            n = ref_pis[j]
            if(m == n):
                #del_inds.append(j)
                del ref_pis[j]
                flag = True
                break
        assert flag, "Pi Symmetries not corect"
    #for ind in del_inds:
    #    del ref_pis[ind]
    assert len(ref_pis) == 1 and ref_pis[0] == pi


def test_game_ended():
    """Tests game end detection logic based on fixed boards."""
    array_end_state_pairs = [
         (np.array([[[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
                   ]), 1, 0),
        (np.array([[[1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],

                  [[-1,-1, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0,-1, 0],
                    [0, 0, 0, 0]],

                   [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],

                   [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
                  ]), 1, 1),
        (np.array([[[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
                  ]), -1, -1),
        (np.array([[[1, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[1, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 0]],

                    [[1, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[1, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
                  ]), -1, -1),
        (np.array([[[1, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 0]],

                    [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 1]]
                  ]), -1, -1)
        ]

    for np_pieces, player, expected_end_state in array_end_state_pairs:
        board, player, game = init_board_from_array(np_pieces, player)
        end_state = game.getGameEnded(board, player)
        assert expected_end_state == end_state, ("expected=%s, actual=%s, board=\n%s" % (expected_end_state, end_state, board))


def test_immutable_move():
    """Test original board is not mutated whtn getNextState() called."""
    board, player, game = init_board_from_moves([1, 2, 3, 4, 56, 23])
    original_board_string = game.stringRepresentation(board)

    new_np_pieces, new_player = game.getNextState(board, 7, -1)

    assert original_board_string == game.stringRepresentation(board)
    assert original_board_string != game.stringRepresentation(new_np_pieces)

def main():
    print("Starting test harness...")
    print("Testing simple moves...")
    test_simple_moves()
    print("Test Pass!!")
    print("Testing cube to list conversion")
    check_cube_to_list_conversion()
    print("Test Pass!!")
    print("Testing list to cube conversion")
    check_list_to_cube_conversion()
    print("Test Pass!!")
    print("Testing overfill handling")
    test_overfull_cube()
    print("Test Pass!!")
    print("Testing valid moves")
    test_get_valid_moves()
    print("Test Pass!!")
    print("Testing symmetries")
    test_symmetries()
    print("Test Pass!!")
    print("Testing game ended")
    test_game_ended()
    print("Test Pass!!")
    print("Testing immutable move")
    test_immutable_move()
    print("Test Pass!!")

if __name__ =="__main__":
    main()
