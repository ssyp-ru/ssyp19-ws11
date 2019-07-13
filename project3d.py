import numpy as np

cordslist = []


# Calculating coordinate
def calculating(m, m2, matrixR, matrixR2, matrixK, matrixK2, C):
    cordslist.clear()

    rkm = matrixR @ np.linalg.inv(matrixK) @ m
    alpha = rkm[0][0]
    beta = rkm[1][0]
    gamma = rkm[2][0]

    rkm = matrixR2 @ np.linalg.inv(matrixK2) @ m2
    alpha2 = rkm[0][0]
    beta2 = rkm[1][0]
    gamma2 = rkm[2][0]

    S = np.array([[1, 0, 0, alpha, 0],
                  [0, 1, 0, beta, 0],
                  [0, 0, 1, gamma, 0],
                  [1, 0, 0, 0, alpha2],
                  [0, 1, 0, 0, beta2],
                  [0, 0, 1, 0, gamma2]])  # S@(X, Y, Z, r1, r2)=C

    Splus = np.linalg.pinv(S)
    solution = Splus @ C
    cordslist.append([])
    cordslist[-1].append(solution[0])
    cordslist[-1].append(solution[1])
    cordslist[-1].append(solution[2])
    return cordslist[-1]


# Creating imaginary line between two dots (a lot of dots between two)
def linear_interpolation(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = p2 - p1
    dots = []
    for i in np.arange(0, 1.1, 0.1):
        answer = (p3 * i + p1).ravel().tolist()
        dots.append(answer)

    return dots
