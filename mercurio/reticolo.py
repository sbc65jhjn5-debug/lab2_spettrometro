import numpy as np
from scipy.stats import chi2

def lamb (theta, sigma_theta, n, d, sigma_d):

    val_lambda = d * np.sin (theta) / n
    sigma_lambda = np.sqrt ((np.sin (theta) / n * sigma_d)**2 + (d * np.cos (theta) / n * sigma_theta)**2)
    return val_lambda, sigma_lambda

if __name__ == "__main__":

    # Dati

    colors = ["viola", "blu", "verde chiaro", "giallo 1", "giallo 2", "rosso"]
    n = 1 # ordine del reticolo
    d = 3322.585 # distanza tra le fenditure in nm (ricavata da "doppietto.py")
    sigma_d = 10.917 # deviazione standard di d (ricavata da "doppietto.py")

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
        print(f"{color}: {mean:.3f} ± {sigma:.3f}")

    # Calcolo di λ e σ_λ

    lambda_rosso, lambda_rosso_sigma = lamb (np.radians(rosso_mean), np.radians(rosso_sigma), n, d, sigma_d)
    lambda_giallo_1, lambda_giallo_1_sigma = lamb (np.radians(giallo_1_mean), np.radians(giallo_1_sigma), n, d, sigma_d)
    lambda_giallo_2, lambda_giallo_2_sigma = lamb (np.radians(giallo_2_mean), np.radians(giallo_2_sigma), n, d, sigma_d)
    lambda_verde_chiaro, lambda_verde_chiaro_sigma = lamb (np.radians(verde_chiaro_mean), np.radians(verde_chiaro_sigma), n, d, sigma_d)
    lambda_blu, lambda_blu_sigma = lamb (np.radians(blu_mean), np.radians(blu_sigma), n, d, sigma_d)
    lambda_viola, lambda_viola_sigma = lamb (np.radians(viola_mean), np.radians(viola_sigma), n, d, sigma_d)

    lambda_values = [lambda_viola, lambda_blu, lambda_verde_chiaro, lambda_giallo_1, lambda_giallo_2, lambda_rosso]
    lambda_sigmas = [lambda_viola_sigma, lambda_blu_sigma, lambda_verde_chiaro_sigma, lambda_giallo_1_sigma, lambda_giallo_2_sigma, lambda_rosso_sigma]
    
    print ("\nValori di λ e deviazioni standard:\n")
    for color, val_lambda, sigma_lambda in zip(colors, lambda_values, lambda_sigmas):
        print(f"λ {color} = {val_lambda:.3f} ± {sigma_lambda:.3f} nm")