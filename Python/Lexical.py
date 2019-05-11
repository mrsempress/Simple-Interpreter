"""
Finish the three tasks of Lexical analyzer:

1. Filter out unwanted components in the source program;
2. Output tokens are used by the parser;
3. Identifies an illegal input and marks it as an "error token."

"""

from enum import Enum
import math
import Exceptions


class TokenType(Enum):
    """
    This class stores all the key words
    """
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    FOR = "FOR"
    FROM = "FROM"
    T = "T"
    SEMICO = ';'
    L_BRACKET = '('
    R_BRACKET = ')'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POWER = '**'
    FUNC = "FUNCTION"
    CONST_ID = 21
    NONTOKEN = 22
    ERRTOKEN = 23


class Token:
    """
    This class stores the information for token
    token - 'TokenType' type
    lexeme - original string of input
    value - corresponding value if it is 'CONST_ID'
    func_ptr - function pointer if it is 'FUNC'
    """

    def __init__(self, token, lexeme="", value=0, func_ptr=None):
        self.token_type = token
        self.string = lexeme
        self.value = value
        self.func_ptr = func_ptr


def my_ln(x):
    """
    :param x: a value
    :return: ln(x)
    """
    return math.log(x, math.e)


def get_token(string):
    """
    :param string: a line of the code
    :return: token types
    """

    print(string)

    ans = []
    now = None
    base = 10
    decimal = 1
    isPoint = False
    isComment = False

    for c in string:

        # comment
        if c == '/' and ans and ans[len(ans)-1].token_type == TokenType.DIV:
            isComment = True
            break

        if c == '-' and ans and ans[len(ans)-1].token_type == TokenType.MINUS:
            isComment = True
            break

        if c.isalpha():
            if now is None:
                now = c
            else:
                now = now + c

        elif c.isdigit():
            if now is None:
                now = int(c)
            elif isinstance(now, float) or isinstance(now, int):
                now = now * base + decimal * int(c)
                if isPoint:
                    decimal *= 0.1
            # deal with words includes number
            else:
                now = now + c
        elif c == '.':
            decimal = 0.1
            base = 1
            isPoint = True

        elif c == '+' or c == '-' or c == '*' or c == '/' or c == '(' or c == ')' or c == ',' or c == ';':
            now = c

        # deal with a complete word
        elif c == ' ':
            flag = False
            for token in TokenType:
                if now == token.value:
                    if now == ';':
                        return ans
                    ans.append(Token(token, lexeme=now))
                    now = None
                    flag = True
                    break

            if flag is False:
                # Function
                if now == "SIN":
                    ans.append(Token(TokenType.FUNC, lexeme="SIN", func_ptr=math.sin))
                    now = None
                elif now == "COS":
                    ans.append(Token(TokenType.FUNC, lexeme="COS", func_ptr=math.cos))
                    now = None
                elif now == "TAN":
                    ans.append(Token(TokenType.FUNC, lexeme="TAN", func_ptr=math.tan))
                    now = None
                elif now == "EXP":
                    ans.append(Token(TokenType.FUNC, lexeme="EXP", func_ptr=math.exp))
                    now = None
                elif now == "SQRT":
                    ans.append(Token(TokenType.FUNC, lexeme="SQRT", func_ptr=math.sqrt))
                    now = None
                elif now == "LN":
                    ans.append(Token(TokenType.FUNC, lexeme="LN", func_ptr=my_ln))
                    now = None

                elif now == "PI":
                    ans.append(Token(TokenType.CONST_ID, lexeme=now, value=math.pi))
                elif now == "E":
                    ans.append(Token(TokenType.CONST_ID, lexeme=now, value=math.e))
                elif now == "T":
                    ans.append(Token(TokenType.T, lexeme=now))

                else:
                    if isinstance(now, str):
                        raise Exceptions.NoMatchingWord("No Such word:", now)
                    elif isinstance(now, float) or isinstance(now, int):
                        ans.append(Token(TokenType.CONST_ID, lexeme=str(now), value=now))
                    elif now is None:
                        continue

                now = None
                base = 10
                decimal = 1
                isPoint = False

    if not isComment:
        raise Exceptions.MissingSemicolon("Missing Semicolon at the end.")
    else:
        print("This is a line of comment.")
        return None


def show(now):
    """
    show the words category
    :param now: the result after lexical analysis
    """

    print("category".ljust(10), "original input".ljust(20), "value".ljust(20), "function pointer")
    for x in now:
        print(x.token_type.name.ljust(10), x.string.ljust(20), format(x.value, "<20"), x.func_ptr)


def preprocess(temp):
    """

    :param temp:
    :return:
    """
    temp = " + ".join(temp.split('+'))
    temp = " / ".join(temp.split('/'))
    temp = " * ".join(temp.split('*'))
    temp = " - ".join(temp.split('-'))
    temp = " , ".join(temp.split(','))
    temp = " ( ".join(temp.split('('))
    temp = " ) ".join(temp.split(')'))
    temp = " ; ".join(temp.split(';'))
    return temp


def scanner():
    """
    This method read codes from "code.txt", analysis the code, show the result
    :return: the result after analysis, which is the basement of grammar
    """
    try:
        lineNum = 1
        with open("code.txt") as fp:
            result = []
            for line in fp.readlines():
                print("Line", lineNum, ":")
                lineNum += 1
                line=line.upper()
                now = get_token(preprocess(line))

                # to get '**' afterwards
                ans = []
                last = None

                # comment skip
                if not now:
                    continue

                for now_token in now:
                    if last is not None and last.token_type == TokenType.MUL and now_token.token_type == TokenType.MUL:
                        ans.pop()
                        ans.append(Token(TokenType.POWER, lexeme='**'))
                        continue

                    last = now_token
                    ans.append(now_token)

                show(ans)
                print()

                result.append(ans)
            return result

    except OSError as e:
        print("LEXICAL EXCEPTION:", e)
    except Exceptions.NoMatchingWord as e:
        print("LEXICAL EXCEPTION:", e.args)
    except Exceptions.MissingSemicolon as e:
        print("LEXICAL EXCEPTION:", e.args)
