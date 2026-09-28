#By Toby Strawser
#Worst run time would be degree n^2 where the given list needed to be sorted and every element compared needed to be flipped.

def bubble_sort(a:list,key = None):
    temp = a
    if key == 'len':
        for i in range(len(a) - 1):
            for j in range(len(a) - 1):
                if len(temp[j]) > len(temp[j + 1]):
                    temp[j + 1], temp[j] = temp[j], temp[j + 1]

    for i in range(len(a)-1):
        for j in range(len(a) - 1):
            if temp[j] > temp[j +1]:
                temp[j+1], temp[j] = temp[j],temp[j+1]
    return temp
