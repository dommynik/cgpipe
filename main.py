import math
import numpy as np
import cgpipe.mtxio
import scipy.sparse as scsp
import scipy.sparse.linalg as scla


def main(matrix_url, hint_filename=None):
    a = cgpipe.mtxio.load_matrix(matrix_url, hint_filename)
    width = a.shape[0]

    solution_x = np.full(width, 1 / math.sqrt(width))

    x = np.zeros(width)
    b = a * solution_x

    diag = 1 / scla.norm(a, 1, 1)
    m = scsp.spdiags(diag, 0, width, width)

    solve_cg(a, b, x, m)


def solve_cg(a, b, x0, m):
    x = x0
    r = b - a * x
    u = m * r
    w = a * u
    p = np.zeros(a.shape[0])
    s = np.zeros(a.shape[0])

    tau = np.linalg.norm(r)
    delta = u.dot(w.transpose())
    gamma = r.dot(u.transpose())
    beta = 0
    alpha = gamma / delta
    k = 0

    while k < a.shape[0] and tau > 1e-50:
        # S1
        p_ = u + beta * p
        s_ = w + beta * s
        x_ = x + alpha * p_
        r_ = r - alpha * s_
        tau_ = np.linalg.norm(r_)
        u_ = m * r_
        w_ = a * u_
        delta_ = w_.dot(u_.transpose())
        gamma_ = r_.dot(u_.transpose())
        beta_ = gamma_ / gamma
        theta = s_.dot(u_.transpose())
        pi_ = delta_ + beta_ * theta
        alpha_ = gamma_ / pi_
        k = k + 1

        p = p_
        s = s_
        x = x_
        r = r_
        tau = tau_
        u = u_
        w = w_
        gamma = gamma_
        beta = beta_
        alpha = alpha_

        print(k, tau)


# main('http://www.cise.ufl.edu/research/sparse/MM/AMD/G3_circuit.tar.gz')
# main('http://www.cise.ufl.edu/research/sparse/MM/Oberwolfach/LFAT5.tar.gz', 'LFAT5.mtx')
# main('http://www.cise.ufl.edu/research/sparse/MM/HB/nos7.tar.gz')
main('http://www.cise.ufl.edu/research/sparse/MM/DNVS/shipsec1.tar.gz')
# main('http://www.cise.ufl.edu/research/sparse/MM/Janna/Flan_1565.tar.gz')
# main('http://www.cise.ufl.edu/research/sparse/MM/Botonakis/thermomech_dM.tar.gz')