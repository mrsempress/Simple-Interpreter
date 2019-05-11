"""
Solve the expression, try to build the grammar tree; then use the tree to calculate some node;
"""

class Node:
    """
    class for the tree node
    """

    def __init__(self, val=None, token=None, func=None):
        self.value = val  # record the value of the expression represented by son, to reduce repetitive work
        self.token = token
        self.func = func
        self.flag = False  # Whether there exists parameter 'T'
        self.left_child = None
        self.right_child = None
        self.height = 0

    def insert_left(self, new_node):
        self.left_child = new_node

    def insert_right(self, new_node):
        self.right_child = new_node

    def preprocess(self, floor):
        """
        Get the height of the expression tree
        """
        self.height = floor
        if self.left_child:
            self.height = max(self.height, self.left_child.preprocess(floor + 1))
        if self.right_child:
            self.height = max(self.height, self.right_child.preprocess(floor + 1))
        return self.height

    def find_T(self):
        """
        Find if there exists parameter T
        """
        if self.token == "T":
            self.flag = True
            return True

        if self.left_child:
            self.flag |= self.left_child.find_T()

        if self.right_child:
            self.flag |= self.right_child.find_T()

        return self.flag

    def traverse(self):
        """
        Output the tree structure
        """
        if self.token == 21:    # Token CONST_ID = 21
            print("CONST_ID", self.value)
        else:
            print(self.token)

        if self.left_child:
            print("left")
            self.left_child.traverse()
            print("back")
        if self.right_child:
            print("right")
            self.right_child.traverse()
            print("back")

    def GetExprValue(self, var=None):
        """
        Calculate the value of expression
        """
        if not self.flag and self.value:
            return self.value

        if self.token == "+":
            self.value = self.left_child.GetExprValue(var) + self.right_child.GetExprValue(var)

        elif self.token == "-":
            self.value = self.left_child.GetExprValue(var) - self.right_child.GetExprValue(var)

        elif self.token == '*':
            self.value = self.left_child.GetExprValue(var) * self.right_child.GetExprValue(var)

        elif self.token == '/':
            self.value = self.left_child.GetExprValue(var) / self.right_child.GetExprValue(var)

        elif self.token == "**":
            self.value = pow(self.left_child.GetExprValue(var), self.right_child.GetExprValue(var))

        elif self.token == "FUNCTION":
            self.value = self.func(self.left_child.GetExprValue(var))

        elif self.token == 'T':
            return var

        return self.value


def expression(token_list):
    root = Node()
    for i in range(1, len(token_list)):
        token = token_list[i].token_type.value
        if token == '+' or token == '-':
            left_child, flag1 = expression(token_list[:i])
            right_child, flag2 = term(token_list[i + 1:])
            if flag1 and flag2:
                root.insert_left(left_child)
                root.insert_right(right_child)
                root.token = token
                return root, True

    return term(token_list)


def term(token_list):
    root = Node()
    for i in range(1, len(token_list)):
        token = token_list[i].token_type.value
        if token == '/' or token == '*':
            left_child, flag1 = term(token_list[:i])
            right_child, flag2 = factor(token_list[i + 1:])
            if flag1 and flag2:
                root.insert_right(right_child)
                root.insert_left(left_child)
                root.token = token
                return root, True

    return factor(token_list)


def factor(token_list):
    """
    Unary operator
    """
    token = token_list[0].token_type.value
    root = Node()
    if token == '+' or token == '-':
        right_child, flag = factor(token_list[1:])
        if flag:
            root.insert_left(Node(val=0, token="CONST_ID"))
            root.token = token
            root.insert_right(right_child)
            return root, True

    return component(token_list)


def component(token_list):
    root = Node()
    for i in range(1, len(token_list)):
        token = token_list[i].token_type.value
        if token == '**':
            left_child, flag1 = atom(token_list[:i])
            right_child, flag2 = component(token_list[i + 1:])
            if flag1 and flag2:
                root.insert_left(left_child)
                root.insert_right(right_child)
                root.token = token
                return root, True

    return atom(token_list)


def atom(token_list):
    token = token_list[0].token_type.value
    # print("atom: " + str(len(token_list)) + " " + str(token))
    if len(token_list) == 1 and token == 21:    # Token CONST_ID = 21
        return Node(val=token_list[0].value, token=token), True
    elif len(token_list) == 1 and token == "T":
        return Node(token=token), True
    else:
        if token_list[0].token_type.value == "(" and token_list[-1].token_type.value == ")":
            return expression(token_list[1:-1])
        elif (token_list[0].token_type.value == "FUNCTION" and
              token_list[1].token_type.value == "(" and token_list[-1].token_type.value == ")"):
            left_child, flag = expression(token_list[2:-1])
            root = Node(token=token, func=token_list[0].func_ptr)
            root.insert_left(left_child)
            return root, flag

    return None, False
