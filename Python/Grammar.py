"""
Replace CONST_ID in statement with EXPRESSION
"""
import Expression
import Exceptions
import Lexical
import matplotlib.pyplot as plt
import numpy as np
import math

# initialization
angle, scale_x, scale_y, origin_x, origin_y = 0, 1, 1, 0, 0


# some function useful
def match_token(token, want):
    """
    Check if it is the wanted words
    :param token:
    :param want:
    :return:
    """
    if token != want:
        raise Exceptions.NoMatchingWord()


def find_index(token_list, want, start=0):
    """
    Find the position of wanted KEY words
    :param token_list:
    :param want:
    :param start:
    :return:
    """
    for i in range(start, len(token_list)):
        token = token_list[i].string
        if token == want:
            return i

    raise Exceptions.NoMatchingWord()


def get_expression(token_list):
    """
    :param token_list:
    :return:
    """
    root, flag = Expression.expression(token_list)

    if not flag:
        raise Exceptions.NoMatchingWord("It is not the right expression")

    return root


# Then check all the statement
def check_origin(token_list):
    """
    To match the structure of ORIGIN statement:
    ORIGIN IS (EXPRESSION(X), EXPRESSION(Y))
    """
    try:
        dir = {}
        match_token(token_list[0].string, "ORIGIN")
        match_token(token_list[1].string, "IS")
        match_token(token_list[2].string, "(")

        s = 3
        t = find_index(token_list, ",", s)
        # print(str(s) + " " + str(t))
        dir['X'] = get_expression(token_list[s:t])

        s = t + 1
        t = len(token_list) - 1
        dir['Y'] = get_expression(token_list[s:t])

        match_token(token_list[t].string, ')')
        # print(token_list[-1].string == ')')

        # change the origin point
        global origin_x, origin_y
        origin_x, origin_y = dir['X'].GetExprValue(), dir['Y'].GetExprValue()

        return dir

    except Exceptions.NoMatchingWord:
        return None


def check_scale(token_list):
    """
    To match the structure of SCALE statement:
    SCALE IS (EXPRESSION(X), EXPRESSION(Y))
    """
    try:
        dir = {}
        match_token(token_list[0].string, "SCALE")
        match_token(token_list[1].string, "IS")
        match_token(token_list[2].string, "(")

        s = 3
        t = find_index(token_list, ",", s)
        dir['X'] = get_expression(token_list[s:t])

        s = t + 1
        t = len(token_list) - 1
        dir['Y'] = get_expression(token_list[s:t])

        match_token(token_list[t].string, ')')
        # print(token_list[-1].string == ')')

        # change the scale
        global scale_y, scale_x
        scale_x, scale_y = dir['X'].GetExprValue(), dir['Y'].GetExprValue()

        return dir

    except Exceptions.NoMatchingWord:
        return None


def check_rot(token_list):
    """
    To match the structure of ROT statement:
    ROT IS EXPRESSION
    """
    try:
        dir = {}
        match_token(token_list[0].string, "ROT")
        match_token(token_list[1].string, "IS")
        dir["ANGLE"] = get_expression(token_list[2:len(token_list)])

        # semantic analysis
        global angle
        angle = dir['ANGLE'].GetExprValue()

        return dir

    except Exceptions.NoMatchingWord:
        return None


def check_for(token_list):
    """
    To match the structure of FOR statement:
    FOR T FROM EXPRESSION TO EXPRESSION STEP EXPRESSION DRAW (EXPRESSION(X), EXPRESSION(Y))
    """
    try:
        dir = {}
        match_token(token_list[0].token_type.value, "FOR")
        match_token(token_list[1].token_type.value, "T")
        match_token(token_list[2].token_type.value, "FROM")

        s = 3
        t = find_index(token_list, "TO", s)
        dir['FROM'] = get_expression(token_list[s:t])

        s = t + 1
        t = find_index(token_list, "STEP", s)
        dir['TO'] = get_expression(token_list[s:t])

        s = t + 1
        t = find_index(token_list, "DRAW", s)
        dir['STEP'] = get_expression(token_list[s:t])

        match_token(token_list[t + 1].string, '(')
        # print(token_list[t + 1].string == '(')

        s = t + 2
        t = find_index(token_list, ',', s)
        dir['X'] = get_expression(token_list[s:t])

        s = t + 1
        t = len(token_list) - 1
        dir['Y'] = get_expression(token_list[s:t])

        match_token(token_list[-1].string, ')')
        # print(token_list[-1].string == ')')

        DrawLoop(dir['FROM'].GetExprValue(), dir['TO'].GetExprValue(), dir['STEP'].GetExprValue(), dir['X'], dir['Y'])
        return dir

    except Exceptions.NoMatchingWord:
        return None


def program():
    """
    Check the statement, and show the pre-order tree
    :return: the right statement
    """
    lines = Lexical.scanner()
    results = []

    for line in lines:
        # match the correct statement
        print()

        dir = check_origin(line)
        if dir:
            results.append(dir)
            print("This is a ORIGIN statement, which matches "
                  "ORIGIN IS (EXPRESSION(X), EXPRESSION(Y))")
            print("<-------------- Structure of ORIGIN Statement -------------->")
            print("*************** Expression Tree of X ***************")
            dir["X"].traverse()
            print("*************** Expression Tree of Y ***************")
            dir["Y"].traverse()
            continue

        dir = check_scale(line)
        if dir:
            results.append(dir)
            print("This is a SCALE statement, which matches "
                  "SCALE IS (EXPRESSION(X), EXPRESSION(Y))")
            print("<-------------- Structure of SCALE Statement -------------->")
            print("*************** Expression Tree of X ***************")
            dir["X"].traverse()
            print("*************** Expression Tree of Y ***************")
            dir["Y"].traverse()
            continue

        dir = check_rot(line)
        if dir:
            results.append(dir)
            print("This is a ROT statement, which matches "
                  "ROT IS EXPRESSION")
            print("<-------------- Structure of ROT Statement -------------->")
            print("*************** Expression Tree of ANGLE ***************")
            dir["ANGLE"].traverse()
            continue

        dir = check_for(line)
        if dir:
            results.append(dir)
            print("This is a FOR statement, which matches "
                  "FOR T FROM EXPRESSION TO EXPRESSION STEP EXPRESSION DRAW (EXPRESSION(X), EXPRESSION(Y))")
            print("<-------------- Structure of FOR Statement -------------->")
            print("*************** Expression Tree of FROM ***************")
            dir["FROM"].traverse()
            print("*************** Expression Tree of TO ***************")
            dir["TO"].traverse()
            print("*************** Expression Tree of STEP ***************")
            dir["STEP"].traverse()
            print("*************** Expression Tree of X ***************")
            dir["X"].traverse()
            print("*************** Expression Tree of Y ***************")
            dir["Y"].traverse()
            continue

        raise Exceptions.NoMatchingWord("Syntax not matched")

    return {"lines": lines, "results": results}


def DrawLoop(START, END, STEP, X, Y):
    """
    Draw the result
    START<=END STEP is positive;
    START>END STEP is negative
    :param START: start arc
    :param END: end arc
    :param STEP: every arc to draw
    :param X: The x axis of the origin point
    :param Y: The y axis of the origin point
    :return:
    """
    if STEP == 0:
        raise Exceptions.MathError("STEP can't be zero")

    if START <= END and STEP < 0:
        raise Exceptions.MathError("START<=END and STEP is negative!")

    if START >= END and STEP > 0:
        raise Exceptions.MathError("START>=END and STEP is positive!")

    x, y = [], []
    X.find_T()
    Y.find_T()

    for T in np.arange(START, END, STEP):
        x.append(X.GetExprValue(T))
        y.append(Y.GetExprValue(T))

    # print(scale_x, scale_y)
    x = np.array(x) * scale_x
    y = np.array(y) * scale_y
    temp = x * math.cos(angle) + y * math.sin(angle)
    y = y * math.cos(angle) - x * math.sin(angle)
    x = temp
    x = x + origin_x
    y = y + origin_y
    # print(x)
    # print(y)
    plt.scatter(x, y, s=1)
