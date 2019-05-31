def transpose(matrix):
    cols = []
    for i in range(len(matrix[0])):
        cols.append('')
    for row in matrix:
        for col, char in enumerate(row):
            cols[col] += char
    return cols
