#Toby Strawser written 9/10/2025
def log(a:float,b:float):
    i = 0
    tot = b
    while tot > 1:
        tot = tot / a
        i += 1
    if tot == 1:
        return i
    else:
        return i -1
