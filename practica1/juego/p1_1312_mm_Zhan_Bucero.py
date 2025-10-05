from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)

def score(state):
    scores = state.scores
        # Evaluation of the state from the point of view of MAX

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

def getNCorners(state: TwoPlayerGameState,corner = 8):
    s = {(1,1),(1,corner),(corner,1),(corner,corner)}
    d = {state.player1.label: 0, state.player2.label: 0}
    
    for  x in s:
        c = state.board.get(x)
        if c is not None:
            d[c]+=1
    
                
    res = d[state.player1.label] - d[state.player2.label]
    
    if state.is_player_max(state.player1):
        return res

    return -res

def moves(state:TwoPlayerGameState):
    return len(state.game.generate_successors(state))

class MySolution1(StudentHeuristic):
    def get_name(self) -> str:
        return "mysolution1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        
        return 64 * getNCorners(state) + 16 * moves(state) + 4 * getBorders(state) + score(state)


# class Solution2(StudentHeuristic):
#     def get_name(self) -> str:
#         return "solution2"

#     def evaluation_function(self, state: TwoPlayerGameState) -> float:
#         # let's use a global function
#         return func_glob(2, state)
