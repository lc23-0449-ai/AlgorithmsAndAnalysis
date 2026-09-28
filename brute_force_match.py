# Team : Owen Eisen, Toby Strawser, Diego

def match(pattern, text):
    m = len(pattern)
    n = len(text)

    for i in range(n - m + 1):
        for j in range(n - m + 1):
            match_found = True
            for a in range(m):
                for b in range(m):
                    if text[i + a][j + b] != pattern[a][b]:
                        match_found = False
                        break
                if not match_found:
                    break
            if match_found:
                return (i, j)
    return None