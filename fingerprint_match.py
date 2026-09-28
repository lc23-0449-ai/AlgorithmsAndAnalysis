# Team : Owen Eisen, Toby Strawser, Diego

def match(pattern, text):
    m = len(pattern)
    n = len(text)

    if m > n:
        return None

    pattern_fp = 0
    for row in pattern:
        for val in row:
            pattern_fp ^= val

    row_fps = []
    for i in range(n - m + 1):
        row_fp = 0
        for a in range(m):
            for b in range(m):
                row_fp ^= text[i + a][b]
        row_fps.append(row_fp)

    for i in range(n - m + 1):
        current_fp = row_fps[i]
        if current_fp == pattern_fp and verify(pattern, text, i, 0):
            return (i, 0)
        for j in range(1, n - m + 1):
            for a in range(m):
                current_fp ^= text[i + a][j - 1]      # remove left
                current_fp ^= text[i + a][j + m - 1]  # add right
            if current_fp == pattern_fp and verify(pattern, text, i, j):
                return (i, j)
    return None

def verify(pattern, text, i, j):
    m = len(pattern)
    for a in range(m):
        for b in range(m):
            if text[i + a][j + b] != pattern[a][b]:
                return False
    return True