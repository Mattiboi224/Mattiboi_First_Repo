
a = 5
b = 10
matrix = [[0 for _ in range(a)] for _ in range(b)]

transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)

matrix[1][0] = 20

print(matrix)



for i in range(b):
    for j in range(a):
        print (i)
        print(j)
        matrix[i][j] = 10

print(matrix[7][2])

print(matrix)