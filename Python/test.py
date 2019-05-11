"""
read code from "Code.txt", and then put the strings to the interpreter
show the pictures of the statements
"""

import matplotlib.pyplot as plt
import Grammar
import Exceptions

# Open code document
print("The code is follows: ")
with open("Code.txt") as fp:
    for line in fp.readlines():
        # 删除分隔符，如\n, \r, \t, ' '
        print(line.strip())

print()

# run the code
print("Begin learning the code, and draw the result.")
try:
    Grammar.program()
    ax = plt.gca()
    plt.xlim(0)
    plt.ylim(0)
    ax.set_aspect("equal")  # set axes per unit length are same
    ax.xaxis.set_ticks_position('top')  # set the number's position of axis
    ax.invert_yaxis()   # make the y axis invert
    plt.show()
except Exceptions.NoMatchingWord as e:
    print("GRAMMAR EXCEPTION:", e.args)


