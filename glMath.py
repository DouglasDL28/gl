def cross_product(V1, V2):
    res = [
        V1[1]*V2[2] - V1[2]*V2[1],
        V1[2]*V2[0] - V1[0]*V2[2],
        V1[0]*V2[1] - V1[1]*V2[0]
        ]

    return res

def dot_product(V1, V2):
    return V1[0] * V2[0] + V1[1] * V2[1] + V1[2] * V2[2]

def normalize(V):
    norm = (V[0]**2 + V[1]**2 + V[2]**2)**0.5

    return V[0]/norm, V[1]/norm, V[2]/norm
