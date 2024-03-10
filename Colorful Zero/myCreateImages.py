import numpy as np


def read_color_coding():
    a = {}
    with open('colorcoding.csv', mode='r') as f:
        first_line = f.readline()
        file_contents = f.readlines()

        for lines in file_contents:
            (k, r, g, b) = lines.rstrip("\n").split(',')
            a[int(k)] = int(r), int(g), int(b)

        return a

def list_3d_color(color_dict, lst):
    # print(color_dict)
    # print(lst)

    ls = []
    diagonal = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            num = lst[i][j]
            for key, value in color_dict.items():
                if num < 0:
                    num *= -1
                    if num == key:
                        ls.append(255 - value)
                else:
                    if num == key:
                        ls.append(value)
                        break

    arr = np.array(ls)
    newarr = arr.reshape(len(lst), len(lst), 3)
    ls = newarr.tolist()

    return ls
