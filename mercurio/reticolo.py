import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.stats import chi2

if __name__ == "__main__":

    # Dati

    colors = ["viola", "blu", "verde chiaro", "giallo 1", "giallo 2", "rosso"]

    viola = np.array([98.27 - 90.5, 98.5 - 90.5, 98.5 - 90.5])
    viola_mean = np.mean(viola)
    viola_sigma = np.std(viola, ddof=1) / np.sqrt(len(viola))

    blu = np.array([98.8 - 90.5, 99.18 - 90.5, 99.167 - 90.5])
    blu_mean = np.mean(blu)
    blu_sigma = np.std(blu, ddof=1) / np.sqrt(len(blu))

    verde_chiaro = np.array([100.83 - 90.5, 101.167 - 90.5, 101 - 90.5])
    verde_chiaro_mean = np.mean(verde_chiaro)
    verde_chiaro_sigma = np.std(verde_chiaro, ddof=1) / np.sqrt(len(verde_chiaro))

    giallo_1 = np.array([101.667 - 90.5, 101.57 - 90.5, 101.55 - 90.5])
    giallo_1_mean = np.mean(giallo_1)
    giallo_1_sigma = np.std(giallo_1, ddof=1) / np.sqrt(len(giallo_1))

    giallo_2 = np.array([101.75 - 90.5, 101.677 - 90.5, 101.65 - 90.5])
    giallo_2_mean = np.mean(giallo_2)
    giallo_2_sigma = np.std(giallo_2, ddof=1) / np.sqrt(len(giallo_2))

    rosso = np.array([102.5 - 90.5, 102.4 - 90.5, 102.467 - 90.5])
    rosso_mean = np.mean(rosso)
    rosso_sigma = np.std(rosso, ddof=1) / np.sqrt(len(rosso))

    for color, mean, sigma in zip(colors, [viola_mean, blu_mean, verde_chiaro_mean, giallo_1_mean, giallo_2_mean, rosso_mean], [viola_sigma, blu_sigma, verde_chiaro_sigma, giallo_1_sigma, giallo_2_sigma, rosso_sigma]):
        print(f"{color}: {mean:.4f} ± {sigma:.4f}")