import numpy as np

def cross_product(V1, V2):
    res = [
        V1[1]*V2[2] - V1[2]*V2[1],
        V1[2]*V2[0] - V1[0]*V2[2],
        V1[0]*V2[1] - V1[1]*V2[0]
        ]

    return res

def dot_product(V1, V2):
    res = 0
    for i in range(len(V1)):
        res += V1[i] * V2[i]
    return res

def multiply(A, B):
    # M x N * N x P = M x P
    nRows_B = len(B) if isinstance(B[0], (int, float)) else len(B[0])
    nCols_B = 1 if isinstance(B[0], (int, float)) else len(B[0])

    # print("B: ", nRows_B, nCols_B)
    # print("A: ", len(A), len(A[0]))

    if len(A[0]) == nRows_B:
        res = []
        for i in range(len(A)):
            row = []

            if nCols_B == 1:
                res.append(dot_product(A[i], B))
            else:
                for j in range(nCols_B):
                    row.append( dot_product(A[i], [x[j] for x in B]) )
                
                res.append(row)

        return res

def normalize(V):
    norm = (V[0]**2 + V[1]**2 + V[2]**2)**0.5

    return V[0]/norm, V[1]/norm, V[2]/norm

def substract(A, B):
    return [A[i] - B[i] for i in range(len(A))]

def transpose(m):
    print(list(map(list,zip(*m))))
    return list(map(list,zip(*m)))

def matrix_minor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def determinant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    det = 0
    for c in range(len(m)):
        det += ((-1)**c)*m[0][c]*determinant(matrix_minor(m,0,c))
    return det

def inverse(m):
    det = determinant(m)
    if len(m) == 2:
        return [
            [m[1][1]/det, -1*m[0][1]/det],
            [-1*m[1][0]/det, m[0][0]/det]
            ]

    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = matrix_minor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * determinant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/det
    return cofactors

# A = [
#     [ 5, 1 ,3], 
#     [ 1, 1 ,1], 
#     [ 1, 2 ,1]
#     ]

# B = [
#     [ 5, 1 ,3], 
#     [ 1, 1 ,1], 
#     [ 1, 2 ,1]
# ]

# print(multiply(A, B))

