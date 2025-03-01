from tkinter import N
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from game import ColorableCliqueGame
import random
import time
import importlib
import game
importlib.reload(game)

colors = [(255, 100, 100), (100, 100, 255)]
_penv = ColorableCliqueGame(300, 300, 6, colors)


def nCr(n, k):
    s = n
    d = 1
    for i in range(1, k):
        s *= (n - i)
        d *= (i + 1)
    return int(s / d)


def draw(env: ColorableCliqueGame, show=True):
    imgdata = env.frame()
    plt.imshow(imgdata)
    # print(np.max(imgdata), np.min(imgdata), np.average(imgdata))
    if(show):
        plt.show()


def checkColor(game: ColorableCliqueGame, color, nocolor, a, b, c, seen):
    # assume (a,b) colored.
    if game.adjecencyMatrix[(a, c)] == color:
        # (a,c) also colored
        # count triangles too.
        if game.adjecencyMatrix[(b, c)] == nocolor:
            if (b, c) not in seen:
                seen[(b, c)] = 1
                # (b,c) is not colored yet.
                return 1
            return 0
        elif game.adjecencyMatrix[(b, c)] == color:
            if (b, c) not in seen:
                seen[(b, c)] = 1
                # (b,c) is not colored yet.
                return 3
            return 0
    # count triangles too.
    elif game.adjecencyMatrix[(a, c)] == nocolor:
        # (a,c) is not colored
        if game.adjecencyMatrix[(b, c)] == color:
            # (b,c) is colored.
            if (a, c) not in seen:
                seen[(a, c)] = 1
                return 1
    return 0


def distinct_cherry_counter(game: ColorableCliqueGame):
    # Go over all distinct triplets of vertices (a,b,c).
    # Count the number of red/blue possible triangles by adding 1 edge.
    # return the score Red - Blue.
    p0Triangles = 0
    p1Triangles = 0
    p0c = -1
    p1c = 1
    nocolor = 0

    seen0 = {}
    seen1 = {}
    for a in range(game.k):
        for b in range(a+1, game.k):
            for c in range(b+1, game.k):
                if game.adjecencyMatrix[(a, b)] == p0c:
                    p0Triangles += checkColor(game,
                                              p0c, nocolor, a, b, c, seen0)
                elif game.adjecencyMatrix[(a, b)] == p1c:
                    p1Triangles += checkColor(game,
                                              p1c, nocolor, a, b, c, seen1)
                else:
                    # (a,b) has no color.
                    if game.adjecencyMatrix[(a, c)] == p0c and game.adjecencyMatrix[(b, c)] == p0c:
                        if (a, b) not in seen0:
                            p0Triangles += 1
                            seen0[(a, b)] = 1
                    elif game.adjecencyMatrix[(a, c)] == p1c and game.adjecencyMatrix[(b, c)] == p1c:
                        if (a, b) not in seen1:
                            p1Triangles += 1
                            seen1[(a, b)] = 1
    return p0Triangles, p1Triangles


def numpy_distinct_cherry_counter(x):
    _penv.loadfrom1D(x)
    return distinct_cherry_counter(_penv)


def cherry_counter(game: ColorableCliqueGame):
    # Go over all distinct triplets of vertices (a,b,c).
    # Count the number of red/blue possible triangles by adding 1 edge.
    # return the score Red - Blue.
    p0Triangles = 0
    p1Triangles = 0
    p0c = -1
    p1c = 1
    nocolor = 0

    seen = {}
    for a in range(game.k):
        for b in range(a+1, game.k):
            for c in range(b+1, game.k):
                if game.adjecencyMatrix[(a, b)] == p0c:
                    p0Triangles += checkColor(game,
                                              p0c, nocolor, a, b, c, seen)
                elif game.adjecencyMatrix[(a, b)] == p1c:
                    p1Triangles += checkColor(game,
                                              p1c, nocolor, a, b, c, seen)
                else:
                    # (a,b) has no color.
                    if game.adjecencyMatrix[(a, c)] == p0c and game.adjecencyMatrix[(b, c)] == p0c:
                        p0Triangles += 1
                    elif game.adjecencyMatrix[(a, c)] == p1c and game.adjecencyMatrix[(b, c)] == p1c:
                        p1Triangles += 1
    return p0Triangles, p1Triangles


def triangle_huristic(game: ColorableCliqueGame):
    """
    A simple huristics function.
    The player who "makes" a triangle first in his turn loses.
    Hence our huristics ask how many triangles each player can create by adding a single edge in his color.
    The player who can create more triangles would have higher chance of lossing.

    This ignores who is the next player to put an edge.
    """
    if(game.winner != -1):
        # Assume that 1 has already won, we return -(1 * 2 - 1) = -1.
        # Assume that 0 has already won, we return -(0 * 2 - 1) = 1
        score = -100 * (game.winner * 2 - 1)
        # return some value much bigger then nCr(k,3)
        return score

    p0Triangles, p1Triangles = distinct_cherry_counter(game)
    # p0Triangles *= p0Triangles
    # p1Triangles *= p1Triangles
    # the more triangles one can make the worse his position is.
    return p1Triangles - p0Triangles


def triangleSQR_huristic(game: ColorableCliqueGame):
    """
    A simple huristics function.
    The player who "makes" a triangle first in his turn loses.
    Hence our huristics ask how many triangles each player can create by adding a single edge in his color.
    The player who can create more triangles would have higher chance of lossing.

    This ignores who is the next player to put an edge.
    """
    if(game.winner != -1):
        # Assume that 1 has already won, we return -(1 * 2 - 1) = -1.
        # Assume that 0 has already won, we return -(0 * 2 - 1) = 1
        score = -100 * (game.winner * 2 - 1)
        # return some value much bigger then nCr(k,3)
        return score

    p0Triangles, p1Triangles = cherry_counter(game)
    # p0Triangles *= p0Triangles
    # p1Triangles *= p1Triangles
    # the more triangles one can make the worse his position is.
    return p1Triangles - p0Triangles


def triangleP0_huristic(game: ColorableCliqueGame):
    """
    A simple huristics function.
    The player who "makes" a triangle first in his turn loses.
    Hence our huristics ask how many triangles each player can create by adding a single edge in his color.
    The player who can create more triangles would have higher chance of lossing.

    This ignores who is the next player to put an edge.
    """
    if(game.winner != -1):
        # Assume that 1 has already won, we return -(1 * 2 - 1) = -1.
        # Assume that 0 has already won, we return -(0 * 2 - 1) = 1
        score = -100 * (game.winner * 2 - 1)
        # return some value much bigger then nCr(k,3)
        return score

    p0Triangles, p1Triangles = distinct_cherry_counter(game)
    # the more triangles one can make the worse his position is.
    # player 0 wants to minimize the number of triangles he have, player 1 tries to maximize the number of triangles player 1 has.
    return - p0Triangles
    # return p1Triangles - p0Triangles


def alphabetaMaxDepth(cliqueGame: ColorableCliqueGame, alpha, beta, depth, huristic_function):
    """
    Run alpha beta on instance.
    Starting params alpha = -9999, beta = 9999
    depth watever.
    huristicsf = huristics function
    """
    bestscore = -99999
    if(cliqueGame.winner != -1):
        # Assume that 1 has already won, we return -(1 * 2 - 1) = -1.
        # Assume that 0 has already won, we return -(0 * 2 - 1) = 1
        score = -100 * (cliqueGame.winner * 2 - 1)
        return score
    if(depth == 0):
        return huristic_function(cliqueGame)

    # curr = cliqueGame.player
    color = -(cliqueGame.player * 2 - 1)  # if player 1 then color = -1
    for move in cliqueGame.getMoves():
        cliqueGame.applyMove(move)

        score = color * 0.975 * \
            alphabetaMaxDepth(cliqueGame, -beta, -alpha,
                              depth-1, huristic_function)
        cliqueGame.undo()

        if(score >= beta):
            return color * score
        if(score > bestscore):
            bestscore = score
        if(score > alpha):
            alpha = score
    # The higher the value the better it is for player 0.
    # generallity 0 > means that 0 wins, and negative values means that player 1 wins.
    return color * bestscore


def alphabeta(node: ColorableCliqueGame, depth, a, b, maximizingPlayer, huristic_function):
    if node.winner != -1:
        # Assume that 1 has already won, we return -(1 * 2 - 1) = -1.
        # Assume that 0 has already won, we return -(0 * 2 - 1) = 1
        score = -100 * (node.winner * 2 - 1)
        # return some value much bigger then nCr(k,3)
        return score

    if depth == 0:
        return huristic_function(node)
    if maximizingPlayer:
        value = -999999
        for move in node.getMoves():
            node.applyMove(move)
            value = max(value, 0.9 * alphabeta(node, depth - 1,
                        a, b, False, huristic_function))
            node.undo()
            if value >= b:
                break  # (* β cutoff *)
            a = max(a, value)
        return value
    else:
        value = 999999
        for move in node.getMoves():
            node.applyMove(move)
            value = min(value, 0.9 * alphabeta(node, depth - 1,
                        a, b, True, huristic_function))
            node.undo()
            if value <= a:
                break  # (* α cutoff *)
            b = min(b, value)
        return value


def random_move(game: ColorableCliqueGame):
    moves = game.getMoves()
    if(len(moves) > 0):
        rm = moves[int(random.random() * len(moves))]
        md = game.applyMove(rm)
        return md
    return game.applyMove(None)


def alphabetaMove(game: ColorableCliqueGame, depth, huristic_func):
    moves = game.getMoves()
    bestmove = None
    bestscore = -99999
    color = -(game.player * 2 - 1)
    for move in moves:
        game.applyMove(move)
        score = color * alphabeta(game, depth, -99999,
                                  99999, game.player == 0, huristic_func)
        #alphabetaMaxDepth(game, -99999, 99999, depth, huristic_func)
        game.undo()
        if score > bestscore:
            bestscore = score
            bestmove = move
    return game.applyMove(bestmove)


indexToMoveMap = {}
MoveToIndexMap = {}

k = 0
for i in range(6):
    for j in range(i+1, 6):
        indexToMoveMap[k] = (i, j)
        MoveToIndexMap[(i, j)] = k
        k += 1


def indexToMove(index):
    return indexToMoveMap[index]


def moveToIndex(move):
    return MoveToIndexMap[move]


def alphabetaMoveRet(game: ColorableCliqueGame, depth, huristic_func):
    moves = game.getMoves()
    bestmove = None
    bestscore = -99999
    color = -(game.player * 2 - 1)
    for move in moves:
        game.applyMove(move)
        score = color * alphabeta(game, depth, -99999,
                                  99999, game.player == 0, huristic_func)
        #alphabetaMaxDepth(game, -99999, 99999, depth, huristic_func)
        game.undo()
        if score > bestscore:
            bestscore = score
            bestmove = move
    return bestmove


def alphabetaMove2(game: ColorableCliqueGame, depth, huristic_func):
    moves = game.getMoves()
    bestmove = None
    bestscore = -99999
    color = -(game.player * 2 - 1)
    for move in moves:
        game.applyMove(move)
        score = color * alphabetaMaxDepth(game, depth, -99999,
                                          99999, huristic_func)
        #alphabetaMaxDepth(game, -99999, 99999, depth, huristic_func)
        game.undo()
        if score > bestscore:
            bestscore = score
            bestmove = move
    return game.applyMove(bestmove)


def Saved(saved, item):
    for s in saved:
        # print(s, item)
        if np.array_equal(s, item, equal_nan=True):
            return True
    return False


def getPsuedoLegalStates():
    allp = []
    size = int(nCr(6, 2))
    state = np.zeros(size).astype(np.int64)
    counter = 0

    def fill(state: np.ndarray, index):
        nonlocal counter
        if index < 0:
            allp.append(state)
            return
        counter += 1
        if counter % 500000 == 0:
            print(counter)
        for i in range(-1, 2):
            ns = state.copy()
            ns[index] = i
            fill(ns, index - 1)

    fill(state, size - 1)
    return allp


def getLegalStatesAndTag(psuedoLegalStates, depth, huristic_function, log=100000):
    X = []
    counter = 0
    colors = [(255, 100, 100), (100, 100, 255)]
    env = ColorableCliqueGame(300, 300, 6, colors)
    for state in psuedoLegalStates:
        if abs(state).sum() < 4:
            continue
        # env.reset()
        counter += 1
        if counter % log == 0:
            print("ab", counter)
            # break
        if env.loadfrom1D(state):
            val = alphabeta(env, depth, -99999,
                            99999, env.player == 0, huristic_function)
            # print(val)
            # print(env.winner)
            # print(alphabetaMaxDepth(env, -9999, 9999, 2))
            X.append([env.state1D(), val])
            # draw(env)
            # break
    X = np.array(list(X))
    return X


def getNextBestMoves(psuedoLegalStates, depth, huristic_function, log=100000):
    X = []
    counter = 0
    colors = [(255, 100, 100), (100, 100, 255)]
    env = ColorableCliqueGame(300, 300, 6, colors)
    for state in psuedoLegalStates:
        if abs(state).sum() < 4:
            continue
        # env.reset()
        counter += 1
        if counter % log == 0:
            print("ab", counter)
            # break
        if env.loadfrom1D(state):
            if env.winner != -1:
                continue
            move = alphabetaMoveRet(env, depth, huristic_function)
            # print(val)
            # print(env.winner)
            # print(alphabetaMaxDepth(env, -9999, 9999, 2))
            X.append([env.state1D(), moveToIndex(move)])
            # draw(env)
            # break
    X = np.array(list(X))
    return X
