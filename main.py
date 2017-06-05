import math

import numpy as np

import cgpipe.mtxio


def main(matrix_url: str, hint_filename: str = None):
    A = cgpipe.mtxio.load_matrix(matrix_url, hint_filename)
    sol_x = np.full((A.shape[0]), 1 / math.sqrt(A.shape[0]))

    x = np.empty((A.shape[0]))
    b = A * sol_x

    solve_cg(A, b, x)


def solve_cg(A, b, xi):
    x = xi
    r = b - A * x
    d = r

    for i in range(1, len(b) + 10):
        z = A * d
        alpha = r.dot(r.transpose()) / d.dot(z.transpose())
        x = x + alpha * d
        rn = r - alpha * z
        beta = rn.dot(rn) / r.dot(r.transpose())
        d = rn + beta * d
        r = rn

        print(np.linalg.norm(r))


# main('http://www.cise.ufl.edu/research/sparse/MM/AMD/G3_circuit.tar.gz')
main('http://www.cise.ufl.edu/research/sparse/MM/Oberwolfach/LFAT5.tar.gz', 'LFAT5.mtx')
