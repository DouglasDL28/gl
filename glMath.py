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
    """ Multiplica A x B. Evalúa si A y B son números, vectores o matrices para realizar la multiplicación. """
    if not isinstance(A, (int, float)):
        # A vector
        if isinstance(A[0], (int, float)):
            if not isinstance(B, (int, float)):
                # B vector
                if isinstance(B[0], (int, float)):
                    return vector_x_vector(A, B)
                # B matriz
                else:
                    return vector_x_matrix(B, A)
            # B número
            else:
                return [B * A[i] for i in range(len(A))]

        # A matriz
        else:
            if not isinstance(B, (int, float)):
                # B vector
                if isinstance(B[0], (int, float)):
                    return vector_x_matrix(A, B)
                # B matriz
                else:
                    return matrix_x_matrix(A, B)
            # B número
            else:
                return num_x_matrix(B, A)

    # A número
    else:
        if not isinstance(B, (int, float)):
            # B vector
            if isinstance(B[0], (int, float)):
                return [A * B[i] for i in range(len(B))]
            # B matriz
            else:
                return num_x_matrix(A, B)
        # B número
        else:
            return A * B


def normalize(V):
    norm_ = norm(V)

    return V[0]/norm_, V[1]/norm_, V[2]/norm_

def substract(A, B):
    if isinstance(A,(int, float)) or isinstance(B,(int, float)):
        if isinstance(A,(int, float)):
            return [B[i] - A for i in range(len(B))]

        elif isinstance(B,(int, float)):
            return [A[i] - B for i in range(len(A))]
        else:
            return A - B
    else:
        return [A[i] - B[i] for i in range(len(A))]

def add(A, B):
    if isinstance(A,(int, float)) or isinstance(B,(int, float)):
        if isinstance(A,(int, float)):
            return [B[i] + A for i in range(len(B))]

        elif isinstance(B,(int, float)):
            return [A[i] + B for i in range(len(A))]
        else:
            return A + B
    else:
        return [A[i] + B[i] for i in range(len(A))]

def transpose(m):
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

def norm(V):
    return (V[0]**2 + V[1]**2 + V[2]**2)**0.5

def matrix_x_matrix(A, B): # A x B
    """ Multiplica A x B con la forma MxN * NxP = MxP. Las columnas de A deben ser igual a las filas de B."""
    nrow_b = len(B)
    ncols_b = len(B[0])

    result = []
    for i in range(len(A)): # filas A
        row = []
        for j in range(ncols_b): # columnas B
            row.append( dot_product(A[i], [x[j] for x in B]) )
        
        result.append(row)

    return result

def vector_x_matrix(M, V):
    """ Multiplica la matriz M por el vector V. Columnas de M deben ser igual a filas (len) de V."""
    result = []
    for i in range(len(M)): # filas M
        result.append(dot_product(M[i], V))

    return result

def vector_x_vector(V1, V2):
    """ Multiplicación de elementos en matriz. """
    return [V1[i] * V2[i] for i in range(len(V1))]

def num_x_matrix(num, M):
    """ Multiplica escalar por una matriz. """

    for j in len(M): #filas
        for i in len(M[0]): #columnas
            M[j][i] = M[j][i] * num

    return M

