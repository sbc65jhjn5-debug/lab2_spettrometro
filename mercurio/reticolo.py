import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares
from scipy.stats import chi2

if __name__ == "__main__":

    # Dati

    colors = ["viola", "blu", "verde chiaro", "giallo 1", "giallo 2", "rosso"]

    viola = np.array([98.27 - 90.5, 98.5 - 90.5, 98.5 - 90.5])
    blu = np.array([98.8 - 90.5, 99.18 - 90.5, 99.167 - 90.5])
    verde_chiaro = np.array([100.83 - 90.5, 101.167 - 90.5, 101 - 90.5])
    giallo_1 = np.array([101.667 - 90.5, 101.57 - 90.5, 101.55 - 90.5])
    giallo_2 = np.array([101.75 - 90.5, 101.677 - 90.5, 101.65 - 90.5])
    rosso = np.array([102.5 - 90.5, 102.4 - 90.5, 102.467 - 90.5])