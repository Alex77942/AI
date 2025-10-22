"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""

from __future__ import annotations  # For Python 3.7

import numpy as np

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function
from tictactoe import TicTacToe
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
)
from tournament import StudentHeuristic, Tournament

def score(state):
    scores = state.scores
    score_difference = scores[0] - scores[1]

    if state.is_player_max(state.player1):
        state_value = score_difference
    elif state.is_player_max(state.player2):
        state_value = - score_difference

    return state_value

def getBorders(state: TwoPlayerGameState, n = 8):
    s = set()
    for col in range(1,n+1):
        s.add((col,n))
        s.add((n,col))

    for row in range(1,n+1):
        s.add((row,1))
        s.add((row,n))

    d = {state.player1.label: 0, state.player2.label: 0}
    
    for pos, value in state.board.items():
        if pos in s:
            if value in d:
                d[value]+=1
                
    res = d[state.player1.label] - d[state.player2.label]
    
    if state.is_player_max(state.player1):
        return res

    return -res

def getNCorners(state: TwoPlayerGameState, n = 8):
    s = {(1,1),(1,n),(n,1),(n,n)}
    d = {state.player1.label: 0, state.player2.label: 0}
    
    for  x in s:
        c = state.board.get(x)
        if c is not None:
            d[c]+=1
    
                
    res = d[state.player1.label] - d[state.player2.label]
    
    if state.is_player_max(state.player1):
        return res

    return -res


def getStability(state: TwoPlayerGameState, n = 8):
    d = {state.player1.label: 0, state.player2.label: 0}
    s = {(1,1),(1,n),(n,1),(n,n)}
        
    for x in s:
        c = state.board.get(x)
        if c is not None:
            for dx,dy in {(0,1),(1,0),(1,1)}:
                nx, ny = x[0]+dx, x[1]+dy
                if (nx,ny) in state.board and state.board[(nx,ny)] == c:
                    d[c] += 1

    res = d[state.player1.label] - d[state.player2.label]

    if state.is_player_max(state.player1):
        return res
    else:
        return -res

def getParity(state: TwoPlayerGameState, n = 8):
    disks = len(state.board)
    progress = disks / (n * n)
        
    scores = state.scores
    disk_difference = scores[0] - scores[1]
        
    weight = 1.0 + (9.0 * progress)
    
    res = weight * disk_difference
        
    if state.is_player_max(state.player1):
        return res
    else:
        return -res
    
class PositionalHeuristic(StudentHeuristic):
    def get_name(self) -> str:
        return "positional_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        
        return 64 * getNCorners(state)  + 4 * getBorders(state) + score(state)


class StabilityHeuristic(StudentHeuristic):
    def get_name(self) -> str:
        return "stability_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float: 

        return 64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state)  + score(state)
    
class ParityHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "parity_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return getParity(state)
    
class StabilityParityHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "stability_parity_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if len(state.board) < 54:
            return 64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state) + score(state)
        return 10*getParity(state) + 64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state) + score(state)

class StabilitySuccessorHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "stability_successor_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return  64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state) + score(state) + 8*len(state.game.generate_successors(state))

  
class Heuristic1(StudentHeuristic):

    def get_name(self) -> str:
        return "dummy"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        
        return n + 4


class Heuristic2(StudentHeuristic):

    def get_name(self) -> str:
        return "random"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return float(np.random.rand())

def create_reversi_match(player1: Player, player2: Player) -> TwoPlayerMatch:

    initial_board = None
    initial_player = player1

    initial_board = (
        ['..B.B..',
         '.WBBW..',
         'WBWBB..',
         '.W.WWW.',
         '.BBWBWB']
    )

    if initial_board is None:
        height, width = 8, 8
    else:
        height = len(initial_board)
        width = len(initial_board[0])
        try:
            initial_board = from_array_to_dictionary_board(initial_board)
        except ValueError:
            raise ValueError('Wrong configuration of the board')
        else:
            print("Successfully initialised board from array")

    game = Reversi(
        player1=player1,
        player2=player2,
        height=height,
        width=width,
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_seconds_per_move=10, gui=False)


def create_tictactoe_match(player1: Player, player2: Player) -> TwoPlayerMatch:

    dim_board = 3
    initial_player = player1

    game = TicTacToe(
        player1=player1,
        player2=player2,
        dim_board=dim_board,
    )

    initial_board = np.zeros((dim_board, dim_board))

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_seconds_per_move=1000, gui=False)


create_match = create_reversi_match
# since these heuristics do not really assume anything about the Reversi game,
# they can also be used for TicTacToe, but this will not be true in general
# create_match = create_tictactoe_match
tour = Tournament(max_depth=3, init_match=create_match, max_evaluation_time=0.5)

# if the strategies are copy-pasted here:
strats = {'opt1': [Heuristic1], 'opt2': [Heuristic2], 'positional_Zhan_Bucero': [PositionalHeuristic],
         'stability_Zhan_Bucero': [StabilityHeuristic], 'parity_Zhan_Bucero': [ParityHeuristic],
         'stability_parity_Zhan_Bucero': [StabilityParityHeuristic], 'stability_successor_Zhan_Bucero': [StabilitySuccessorHeuristic]}
# if the strategies should be loaded from files in a specific folder:
# folder_name = "folder_strat" # name of the folder where the strategy files are located
# strats = tour.load_strategies_from_folder(folder=folder_name, max_strat=3)

n = 5
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=False,
)

print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)

# print(totals)
# print(scores)

print('\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2 or name2 not in scores[name1]:
            print('\t---', end='')
        else:
            print('\t%d' % (scores[name1][name2]), end='')
    print()
