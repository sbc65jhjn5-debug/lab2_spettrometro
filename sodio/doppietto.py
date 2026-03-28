import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares  
from scipy.stats import chi2

def d (theta, n, lamb):
    return n * lamb / np.sin (theta)

def sigma_d (theta, sigma_theta, n, lamb):
    add1 = n / np.sin (theta) * sigma_theta
    add2 = - n * lamb * np.cos (theta) / np.sin (theta)**2 * sigma_theta
    return np.sqrt (add1**2 + add2**2)

if __name__ == "__main__":

    # Dati
    n_vals = [0, 1, 2, 3, 4]

    deg_0 = 0.0

    deg_1 = [99.9167 - 90, 90 - 78.5333, 99.333 - 90, 100 - 90, 99.25 - 90]
    deg_1_mean = np.mean (deg_1)
    sigma_1 = np.std (deg_1) / np.sqrt (len (deg_1))

    deg_2 = [110.2 - 90, 110.4167 - 90, 90 - 68.333, 110.2 - 90, 109.5 - 90]
    deg_2_mean = np.mean (deg_2)
    sigma_2 = np.std (deg_2) / np.sqrt (len (deg_2))

    deg_3 = [122.0833 - 90, 90 - 56.9, 121.333 - 90, 121.45 - 90, 121.5 - 90]
    deg_3_mean = np.mean (deg_3)
    sigma_3 = np.std (deg_3) / np.sqrt (len (deg_3))

    deg_4 = [135.5 - 90, 90 - 43.8333, 135.3168 - 90, 134.9667 - 90, 134.783 - 90]
    deg_4_mean = np.mean (deg_4)
    sigma_4 = np.std (deg_4) / np.sqrt (len (deg_4))

    print ("\nValori angoli e deviazioni standard:\n")
    for n, deg, sig in zip (n_vals, [deg_0, deg_1_mean, deg_2_mean, deg_3_mean, deg_4_mean], [0, sigma_1, sigma_2, sigma_3, sigma_4]):
        print (f"n = {n}, deg = {deg:.3f} ± {sig:.3f}")

    lambda_mean = np.mean ([588.995, 589.594]) # nanometri

    d_1 = d (np.radians (deg_1_mean), 1, lambda_mean)
    sigma_d_1 = sigma_d (np.radians (deg_1_mean), np.radians (sigma_1), 1, lambda_mean)

    d_2 = d (np.radians (deg_2_mean), 2, lambda_mean)
    sigma_d_2 = sigma_d (np.radians (deg_2_mean), np.radians (sigma_2), 2, lambda_mean)
    
    d_3 = d (np.radians (deg_3_mean), 3, lambda_mean)
    sigma_d_3 = sigma_d (np.radians (deg_3_mean), np.radians (sigma_3), 3, lambda_mean)

    d_4 = d (np.radians (deg_4_mean), 4, lambda_mean)
    sigma_d_4 = sigma_d (np.radians (deg_4_mean), np.radians (sigma_4), 4, lambda_mean)

    print ("\nValori d e deviazioni standard:\n")
    for n, d_val, sig in zip (n_vals[1:], [d_1, d_2, d_3, d_4], [sigma_d_1, sigma_d_2, sigma_d_3, sigma_d_4]):
        print (f"n = {n}, d = {d_val:.3f} ± {sig:.3f}")

    # NB per il calcolo di d, usiamo la media pesata
    d_mean = np.average ([d_1, d_2, d_3, d_4], weights = [1/sigma_d_1**2, 1/sigma_d_2**2, 1/sigma_d_3**2, 1/sigma_d_4**2])
    sigma_d_mean = np.sqrt (1 / (1/sigma_d_1**2 + 1/sigma_d_2**2 + 1/sigma_d_3**2 + 1/sigma_d_4**2))

    print (f"\nValore medio di d: {d_mean:.3f} ± {sigma_d_mean:.3f}\n")