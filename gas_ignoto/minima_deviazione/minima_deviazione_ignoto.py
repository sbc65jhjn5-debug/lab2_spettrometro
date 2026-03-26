import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.stats import chi2
import os

def n (delta, alpha):

    return np.sin ((alpha + delta) / 2) / np.sin (alpha / 2)

def cauchy_inv (y, a, b):

    return np.sqrt (b / (y - a))


def func (x):
    return x


if __name__ == "__main__":

    with open(os.path.join(os.path.dirname(__file__), "angoli_giallo.txt")) as g_input:
        giallo = [float (deg) * np.pi / 180 for deg in g_input.readlines ()]

    with open(os.path.join(os.path.dirname(__file__), "angoli_verde.txt")) as v_input:
        verde = [float (deg) * np.pi / 180 for deg in v_input.readlines ()]

    with open(os.path.join(os.path.dirname(__file__), "angoli_blu.txt")) as b_input:
        blu = [float (deg) * np.pi / 180 for deg in b_input.readlines ()]

    with open(os.path.join(os.path.dirname(__file__), "angoli_rosso.txt")) as r_input:
        rosso = [float (deg) * np.pi / 180 for deg in r_input.readlines ()]


    colors = ["rosso", "giallo", "verde", "blu"]
    colors_mean = []
    colors_sigma = []

    colors_mean.append (np.mean (rosso))
    colors_mean.append (np.mean (giallo))
    colors_mean.append (np.mean (verde))
    colors_mean.append (np.mean (blu))

    colors_sigma.append (np.std (rosso))
    colors_sigma.append (np.std (giallo))
    colors_sigma.append (np.std (verde))
    colors_sigma.append (np.std (blu))

    print ("\nColori, angolo di deviazione minima e incertezza:")
    for col, deg, err in zip (colors, colors_mean, colors_sigma):
        print (f"{col}: {deg} ± {err}")

    # Calcolo degli n

    alpha = float (59.8018 * np.pi / 180)
    sigma_alpha = float (0.30397375 * np.pi / 180)

    colors_n = [n (delta, alpha) for delta in colors_mean]

    def sigma_n (d, sigma_d, a, sigma_a):

        add1 = (np.cos ((a + d) / 2) * np.sin (a / 2) / 2 - np.sin ((a + d) / 2) * np.cos (a / 2) / 2) / np.sin (a / 2)**2

        add2 = (np.cos ((a + d) / 2) / 2) / np.sin (a / 2)

        s = np.sqrt ((add1 * sigma_d)**2 + (add2 * sigma_a)**2)

        return s

    colors_n_sigma = [sigma_n (delta, sigma_delta, alpha, sigma_alpha) for delta, sigma_delta in zip (colors_mean, colors_sigma)]

    print ("\nn:")
    for col, n_val, n_sig in zip (colors, colors_n, colors_n_sigma):
        print (f"{col}: {n_val:.4f} ± {n_sig:.4f}")

    
    # Calcolo lambda

    lambdas = []
    lambdas_sigma = []

    a = 1.597
    sigma_a = 0.009
    b = 7433
    sigma_b = 2322

    for n_val in colors_n:
        lambdas.append (cauchy_inv (n_val, a, b))

    def lamb_sigma (y, sigma_y, a, sigma_a, b, sigma_b):

        add1 = 1 / (np.sqrt (b / (y - a)) * 2 * (y - a))
        add2 = b / (np.sqrt (b / (y - a)) * 2 * (y - a)**2)
        add3 = - b / (np.sqrt (b / (y - a)) * 2 * (y - a)**2)

        s = np.sqrt ((add1 * sigma_b)**2 + (add2 * sigma_a)**2 + (add3 * sigma_y)**2)
        return s

    for n_vals, sigma_n in zip (colors_n, colors_n_sigma):
        lambdas_sigma.append (lamb_sigma (n_vals,
                                          sigma_n,
                                          a,
                                          sigma_a,
                                          b,
                                          sigma_b
                                          ))

    print ("\nLambda:")
    for col, l, sig in zip (colors, lambdas, lambdas_sigma):
        print (f"{col}: {l:.4f} ± {sig:.4f}")
