import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

def compare (gas, ignoto, sigma):

    diff = [(g - i)**2 / s**2 for g, i, s in zip (gas, ignoto, sigma)]

    chi_quadro = np.sum (diff)
    dof = len (gas) - 1
    p_value = chi2.sf (chi_quadro, dof)

    return chi_quadro, dof, p_value


if __name__ == "__main__":

    rosso_ignoto = 780.5115
    sigma_rosso_ignoto = 335.8858
    giallo_ignoto = 677.5714
    sigma_giallo_ignoto = 225.9965
    verde_ignoto = 603.7090
    sigma_verde_ignoto = 169.9630
    blu_ignoto = 451.7410
    sigma_blu_ignoto = 92.0307

    colors = ["rosso", "giallo", "verde", "blu"]
    colors_ignoto = [rosso_ignoto, giallo_ignoto, verde_ignoto, blu_ignoto]
    colors_ignoto_sigma = [sigma_rosso_ignoto, sigma_giallo_ignoto, sigma_verde_ignoto, sigma_blu_ignoto]

    # Colori elio

    rosso_elio = np.mean ([706.5, 728.1])
    giallo_elio = np.mean ([587.6, 667.8])
    verde_elio = 501.6
    blu_elio = 447.1

    colors_elio = [rosso_elio, giallo_elio, verde_elio, blu_elio]

    # Colori argon

    rosso_argon = np.mean ([912.3, 965.8])
    giallo_argon = np.mean ([750.4, 763.5, 794.8, 800.6, 801.5, 810.4, 811.5])
    verde_argon = np.mean ([696.5, 706.7])
    blu_argon = np.mean ([434.8, 461.0, 488.0, 472.7, 476.7, 480.6, 487.9])

    colors_argon = [rosso_argon, giallo_argon, verde_argon, blu_argon]

    # Colori neon

    rosso_neon = np.mean ([603, 607.4, 614.3, 616.4, 621.7, 626.7, 638.3, 640.2, 650.7, 660, 693, 703.2, 717.4, 724.5])
    giallo_neon = 585.3
    verde_neon = np.mean ([501.6, 540.1])
    blu_neon = 0

    colors_neon = [rosso_neon, giallo_neon, verde_neon, blu_neon]

    # Colori Kripton

    rosso__kripton = np.mean ([642.0, 729, 740.7, 760.2])
    giallo_kripton = 0
    verde_kripton = np.mean ([557, 587.1])
    blu_kripton = np.mean ([435.6, 461.9, 465.9, 473.9, 476.6, 483.2, 484.7])

    colors_kripton = [rosso__kripton, giallo_kripton, verde_kripton, blu_kripton]

    # Colori Xenon

    rosso_xenon = 699.1
    giallo_xenon = np.mean ([597.7, 605.1, 609.8])
    verde_xenon = np.mean ([529.2, 541.9])
    blu_xenon = 484.4

    colors_xenon = [rosso_xenon, giallo_xenon, verde_xenon, blu_xenon]

    # Colori co2

    rosso_co2 = 0
    giallo_co2 = 0
    verde_co2 = 0
    blu_co2 = 0

    colors_co2 = [rosso_co2, giallo_co2, verde_co2, blu_co2]


    # Confronto con elio
    chi_quadro_elio, dof_elio, p_value_elio = compare (colors_elio, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con elio: chi^2 = {chi_quadro_elio:.2f}, dof = {dof_elio}, p-value = {p_value_elio:.4f}")

    # Confronto con argon
    chi_quadro_argon, dof_argon, p_value_argon = compare (colors_argon, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con argon: chi^2 = {chi_quadro_argon:.2f}, dof = {dof_argon}, p-value = {p_value_argon:.4f}")

    # Confronto con neon   
    chi_quadro_neon, dof_neon, p_value_neon = compare (colors_neon, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con neon: chi^2 = {chi_quadro_neon:.2f}, dof = {dof_neon}, p-value = {p_value_neon:.4f}")

    # Confronto con kripton
    chi_quadro_kripton, dof_kripton, p_value_kripton = compare (colors_kripton, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con kripton: chi^2 = {chi_quadro_kripton:.2f}, dof = {dof_kripton}, p-value = {p_value_kripton:.4f}")

    # Confronto con xenon
    chi_quadro_xenon, dof_xenon, p_value_xenon = compare (colors_xenon, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con xenon: chi^2 = {chi_quadro_xenon:.2f}, dof = {dof_xenon}, p-value = {p_value_xenon:.4f}")

    # Confronto con co2
    chi_quadro_co2, dof_co2, p_value_co2 = compare (colors_co2, colors_ignoto, colors_ignoto_sigma)
    print (f"Confronto con CO2: chi^2 = {chi_quadro_co2:.2f}, dof = {dof_co2}, p-value = {p_value_co2:.4f}")