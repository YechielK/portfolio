def check(arr, col):
    for i in list(range(1,col+1)):
        if ((arr[col] == arr[col - i]) 
        or (arr[col] == arr[col-i] + i) 
        or (arr[col] == arr[col-i] - i)):
            return False
    return True
    

def solve():
    dict = []
    size = 8
    col = 0
    counter = 0
    b = [0] * size
    while col >= 0:
        col += 1
        if (col == size):
            print(counter, b)
            # dict[counter] = b.copy()
            dict.append(b.copy())
            col -= 1
            counter += 1
        else:
            b[col] = -1
        while col >= 0:
            b[col] += 1
            if (b[col] == size):
                col -= 1
            else:
                if (check(b, col)):
                    break  
    print(dict)
    return dict