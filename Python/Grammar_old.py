"""
Check the grammar is right or not.
Not deal with expression, only use the simple const_ID
"""

import Exceptions
import Lexical


def check_brackets(lines):
    """
    :param lines: lists of codes
    :return: if brackets are not matched, then raise error
    """
    line_number = 0

    if lines is None:
        exit()

    for line in lines:
        stack = []
        line_number += 1
        for token in line:
            if token.token_type == Lexical.TokenType.L_BRACKET:
                stack.append('(')
            elif token.token_type == Lexical.TokenType.R_BRACKET:
                if len(stack) == 0:
                    raise Exceptions.BracketException("BracketException in line",
                                                      line_number, ", missing left bracket.")
                elif stack.pop() != '(':
                    raise Exceptions.BracketException("BracketException in line",
                                                      line_number, ", missing right bracket.")

        if len(stack) != 0:
            raise Exceptions.BracketException("BracketException in line", line_number, ", missing right bracket.")


def check_origin(line, line_number):
    """
    :param line: A line of code
    :param line_number: The number of line
    :return: check if it matches --- ORIGIN IS (CONST_ID,CONST_ID)
    """

    check_list = [Lexical.TokenType.ORIGIN, Lexical.TokenType.IS, Lexical.TokenType.L_BRACKET,
                  Lexical.TokenType.CONST_ID, Lexical.TokenType.COMMA, Lexical.TokenType.CONST_ID,
                  Lexical.TokenType.R_BRACKET]

    length = len(check_list)
    idx = 0
    for token in line:
        if token.token_type == check_list[idx]:
            idx += 1
        if idx == length:
            break

    if idx != length:
        raise Exceptions.LexicalWrong("Syntax not matched exception in line", line_number)
    else:
        print("This is a ORIGIN statement.")


def check_scale(line, line_number):
    """
    :param line: A line of code
    :param line_number: The number of line
    :return: check if it matches --- SCALE IS (CONST_ID,CONST_ID)
    """

    check_list = [Lexical.TokenType.SCALE, Lexical.TokenType.IS, Lexical.TokenType.L_BRACKET,
                  Lexical.TokenType.CONST_ID, Lexical.TokenType.COMMA, Lexical.TokenType.CONST_ID,
                  Lexical.TokenType.R_BRACKET]

    length = len(check_list)
    idx = 0
    for token in line:
        if token.token_type == check_list[idx]:
            idx += 1
        if idx == length:
            break

    if idx != length:
        raise Exceptions.LexicalWrong("Syntax not matched exception in line", line_number)
    else:
        print("This is a SCALE statement.")


def check_rot(line, line_number):
    """
    :param line: A line of code
    :param line_number: The number of line
    :return: check if it matches --- ROT IS CONST_ID
    """

    check_list = [Lexical.TokenType.ROT, Lexical.TokenType.IS, Lexical.TokenType.CONST_ID]

    length = len(check_list)
    idx = 0
    for token in line:
        if token.token_type == check_list[idx]:
            idx += 1
        if idx == length:
            break

    if idx != length:
        raise Exceptions.SyntaxNotMatched("Syntax not matched exception in line", line_number)
    else:
        print("This is a ROT statement.")


def check_for(line, line_number):
    """
    :param line: A line of code
    :param line_number: The number of line
    :return: check if it matches --- FOR T FROM CONST_ID TO CONST_ID STEP CONST_ID DRAW (T,T)
    """

    check_list = [Lexical.TokenType.FOR, Lexical.TokenType.T, Lexical.TokenType.FROM, Lexical.TokenType.CONST_ID,
                  Lexical.TokenType.TO, Lexical.TokenType.CONST_ID, Lexical.TokenType.STEP, Lexical.TokenType.CONST_ID,
                  Lexical.TokenType.DRAW, Lexical.TokenType.L_BRACKET, Lexical.TokenType.T, Lexical.TokenType.COMMA,
                  Lexical.TokenType.T, Lexical.TokenType.R_BRACKET]

    length = len(check_list)
    idx = 0
    for token in line:
        if token.token_type == check_list[idx]:
            idx += 1
        if idx == length:
            break

    if idx != length:
        raise Exceptions.LexicalWrong("Syntax not matched exception in line", line_number)
    else:
        print("This is a FOR statement.")


def check_grammar(lines):
    try:
        check_brackets(lines)

        line_number = 0
        for line in lines:
            line_number += 1
            if line[0].token_type == Lexical.TokenType.FOR:
                check_for(line, line_number)
            elif line[0].token_type == Lexical.TokenType.ROT:
                check_rot(line, line_number)
            elif line[0].token_type == Lexical.TokenType.SCALE:
                check_scale(line, line_number)
            elif line[0].token_type == Lexical.TokenType.ORIGIN:
                check_origin(line, line_number)

    except Exceptions.MissingBracket as e:
        print("GRAMMAR EXCEPTION:", e.args)
    except Exceptions.MissingBracket as e:
        print("GRAMMAR EXCEPTION:", e.args)
