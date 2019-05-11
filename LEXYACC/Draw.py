import matplotlib.pyplot as plt

def draw(X, Y):
    # print(X)
    # print(Y)
    plt.scatter(X, Y, s=1)

def show():
    f = open("output.txt","r")

    X = list()
    Y = list()


    for c in f.readline():
        x = 0
        y = 0
        flag = 0
        for i in c:
            print(i)
            if(i == '\n'):
                break
            if i == ' ':
                flag = 1

            if i > '9' or i < '0':
                continue

            if flag == 0:
                x = x * 10 + (int)(i)
            else:
                y = y * 10 + (int)(i)

            print("!!!")

        print(x)
        print(y)
        X.append(x)
        Y.append(y)

    draw(X, Y)
    # while line:
    #     if line == '\n' or line == ' ' or line == '\t':
    #         break
    #     line = f.readline()
    #     if  len(line) == 0 or line[0].isspace():
    #         break
    #     draw(line[0], line[2])
    f.close()

    ax = plt.gca()
    plt.xlim(0)
    plt.ylim(0)
    ax.set_aspect("equal")

    plt.show()

show()