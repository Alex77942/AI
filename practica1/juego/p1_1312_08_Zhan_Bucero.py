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

class StabilityParityHeuristic(StudentHeuristic):

    def get_name(self) -> str:
        return "stability_parity_Zhan_Bucero"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if len(state.board) < 54:
            return 64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state) + score(state)
        return 10*getParity(state) + 64 * getNCorners(state) + 10 * getStability(state) + 4 * getBorders(state) + score(state)

