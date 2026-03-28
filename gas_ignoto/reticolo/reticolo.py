import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.stats import chi2

def lamb (theta, sigma_theta, d, sigma_d, n):
    l = d * np.sin (theta) / n
    sigma_l = np.sqrt ((np.sin (theta) / n * sigma_d)**2 + (d * np.cos (theta) / n * sigma_theta)**2)
    return l, sigma_l

if __name__ == "__main__":

    # Dati

    n = 1

    colors = ["viola_1", "viola_2", "blu_1", "blu_2", "verde", "giallo"]

    deg_viola_1 = np.array ([90.5 - 85.466, 90.5 - 85.4333, 90.5 - 84, 98.7666 - 90.5, 98.85 - 90.5, 98.5 - 90.5])
    deg_viola_2 = np.array ([90.5 - 85.4667, 90.5 - 85.3839, 90.5 - 83.9, 98.9 - 90.5, 99 - 90.5, 98.4666 - 90.5]) # leggermente più intenso del "viola_1"

    deg_blu_1 = np.array ([90.5 - 85.1667, 90.5 - 82.88, 90.5 - 83.633, 99.1667 - 90.5, 99.28 - 90.5, 98.72 - 90.5]) # leggermemente più intenso del "blu_2"
    deg_blu_2 = np.array ([90.5 - 85.45, 90.5 - 82.8, 90.5 - 83.5, 99.133 - 90.5, 99.3 - 90.5, 98.75 - 90.5])

    deg_verde = np.array ([90.5 - 83.2, 90.5 - 81, 90.5 - 81.6167, 101 - 90.5, 101.12 - 90.5, 100.87 - 90.5]) # intenso

    deg_giallo = np.array ([90.5 - 82.5832, 90.5 - 80.5, 90.5 - 81.1667, 101.566 - 90.5, 101.33 - 90.5, 101.3 - 90.5]) # intenso

    # medie
    deg_viola_1_mean = np.mean (deg_viola_1)
    deg_viola_2_mean = np.mean (deg_viola_2)
    deg_blu_1_mean = np.mean (deg_blu_1)
    deg_blu_2_mean = np.mean (deg_blu_2)
    deg_verde_mean = np.mean (deg_verde)
    deg_giallo_mean = np.mean (deg_giallo)

    # sigma
    deg_viola_1_sigma = np.std (deg_viola_1, ddof = 1) / np.sqrt (len (deg_viola_1))
    deg_viola_2_sigma = np.std (deg_viola_2, ddof = 1) / np.sqrt (len (deg_viola_2))
    deg_blu_1_sigma = np.std (deg_blu_1, ddof = 1) / np.sqrt (len (deg_blu_1))
    deg_blu_2_sigma = np.std (deg_blu_2, ddof = 1) / np.sqrt (len (deg_blu_2))
    deg_verde_sigma = np.std (deg_verde, ddof = 1) / np.sqrt (len (deg_verde))
    deg_giallo_sigma = np.std (deg_giallo, ddof = 1) / np.sqrt (len (deg_giallo))

    print ("\nMedie e incertezze sui gradi:\n")
    for color, deg_mean, deg_sigma in zip (colors, [deg_viola_1_mean, deg_viola_2_mean, deg_blu_1_mean, deg_blu_2_mean, deg_verde_mean, deg_giallo_mean], [deg_viola_1_sigma, deg_viola_2_sigma, deg_blu_1_sigma, deg_blu_2_sigma, deg_verde_sigma, deg_giallo_sigma]):
        print (f"{color}: {deg_mean:.4f} ± {deg_sigma:.4f} gradi")

    # Calcolo lambda e incertezze

    d = 3322.585 # distanza tra le fenditure in nm (ricavata da "mercurio/doppietto.py")
    sigma_d = 10.917 # deviazione standard di d (ricavata da "mercurio/doppietto.py")
    n = 1 # ordine del reticolo

    lambda_viola_1, lambda_viola_1_sigma = lamb (np.radians (deg_viola_1_mean), np.radians (deg_viola_1_sigma), d, sigma_d, n)
    lambda_viola_2, lambda_viola_2_sigma = lamb (np.radians (deg_viola_2_mean), np.radians (deg_viola_2_sigma), d, sigma_d, n)
    lambda_blu_1, lambda_blu_1_sigma = lamb (np.radians (deg_blu_1_mean), np.radians (deg_blu_1_sigma), d, sigma_d, n)
    lambda_blu_2, lambda_blu_2_sigma = lamb (np.radians (deg_blu_2_mean), np.radians (deg_blu_2_sigma), d, sigma_d, n)
    lambda_verde, lambda_verde_sigma = lamb (np.radians (deg_verde_mean), np.radians (deg_verde_sigma), d, sigma_d, n)
    lambda_giallo, lambda_giallo_sigma = lamb (np.radians (deg_giallo_mean), np.radians (deg_giallo_sigma), d, sigma_d, n)

    print ("\nValori di λ e deviazioni standard:\n")
    for color, val_lambda, sigma_lambda in zip (colors, [lambda_viola_1, lambda_viola_2, lambda_blu_1, lambda_blu_2, lambda_verde, lambda_giallo], [lambda_viola_1_sigma, lambda_viola_2_sigma, lambda_blu_1_sigma, lambda_blu_2_sigma, lambda_verde_sigma, lambda_giallo_sigma]):
        print (f"λ {color} = {val_lambda:.3f} ± {sigma_lambda:.3f} nm")