import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# CIAO, SONO VALE
# DEVO FINIRE DI CONTROLLARE COME MAI IL CHI QUADRO CON IL RETICOLO FACCIA CAGARE CON L'ELIO,
# PRESUMO CI SIA UN ERRORE NEI DATI DELLE LUNGHEZZE D'ONDA... o magari non è Elio, BAH...
# IO HO PRESO I DATI DAL SITO (per viola e alcuni blu, mentre le altre sono dal sito dell'altra volta)
# https://physics.nist.gov/PhysRefData/ASD/Html/lineshelp.html
# DOPO FINISCO DI CONTROLLARLE
# forse è meglio se prendiamo tutti i dati dallo stesso sito? ma non dovrebbe cambiare in realtà...
# COMUNQUE SICURO PIUTTOSTO CHE IL CHI QUADRO MEGLIO IL POWER TEST

def compare (gas, ignoto, sigma):

    diff = [(g - i)**2 / s**2 for g, i, s in zip (gas, ignoto, sigma)]

    chi_quadro = np.sum (diff)
    dof = len (gas) - 1
    p_value = chi2.sf (chi_quadro, dof)

    return chi_quadro, dof, p_value


if __name__ == "__main__":

    # Con prisma, abbiamo ottenuto i seguenti valori di λ (con relative deviazioni standard):

    rosso_ignoto_p = 780.5115 # sus... oltre lo spettro visibile...
    sigma_rosso_ignoto_p = 335.8858
    giallo_ignoto_p = 677.5714 # sus... nel rosso
    sigma_giallo_ignoto_p = 225.9965
    verde_ignoto_p = 603.7090 # sus... nel giallo
    sigma_verde_ignoto_p = 169.9630
    blu_ignoto_p = 451.7410 # ok, nel blu
    sigma_blu_ignoto_p = 92.0307

    # Con reticolo, abbiamo ottenuto i seguenti valori di λ (con relative deviazioni standard):

    giallo_ignoto_r = 576.448
    sigma_giallo_ignoto_r = 28.137
    verde_ignoto_r = 550.037
    sigma_verde_ignoto_r = 30.003
    blu1_ignoto_r = 438.351 # leggermente più intenso del blu2
    sigma_blu1_ignoto_r = 30.79 
    blu2_ignoto_r = 437.833
    sigma_blu2_ignoto_r = 32.882
    viola1_ignoto_r = 397.412
    sigma_viola1_ignoto_r = 36.704
    viola2_ignoto_r = 401.237 # leggermente più intenso del viola1
    sigma_viola2_ignoto_r = 37.473

    # oss: giallo, verde, viola1, viola2 sono nei rispettivi spettri,
    #      mentre il rosso era sottilissimo (quindi non lo abbiamo preso),
    #      il blu è leggermente più verso il viola rispetto ai valori teorici, ma potrebbe starci perché erano praticamente attaccati

    # Procediamo al confronto con gas nobili e co2, usando i valori di λ ottenuti con il prisma e con il reticolo (con relative deviazioni standard):

    colors_p = ["rosso", "giallo", "verde", "blu"]
    colors_ignoto_p = [rosso_ignoto_p, giallo_ignoto_p, verde_ignoto_p, blu_ignoto_p]
    colors_ignoto_sigma_p = [sigma_rosso_ignoto_p, sigma_giallo_ignoto_p, sigma_verde_ignoto_p, sigma_blu_ignoto_p]

    colors_r = ["giallo", "verde", "blu 1", "blu 2", "viola 1", "viola 2"]
    colors_ignoto_r = [giallo_ignoto_r, verde_ignoto_r, blu1_ignoto_r, blu2_ignoto_r, viola1_ignoto_r, viola2_ignoto_r]
    colors_ignoto_sigma_r = [sigma_giallo_ignoto_r, sigma_verde_ignoto_r, sigma_blu1_ignoto_r, sigma_blu2_ignoto_r, sigma_viola1_ignoto_r, sigma_viola2_ignoto_r]

    # Colori elio

    rosso_elio = np.mean ([706.5, 728.1])
    giallo_elio = np.mean ([587.6, 667.8])
    verde_elio = 501.6
    blu_elio = 447.1
    viola1_elio = 388.9 
    viola2_elio = 402.6

    colors_elio_p = [rosso_elio, giallo_elio, verde_elio, blu_elio]
    colors_elio_r = [giallo_elio, verde_elio, blu_elio, blu_elio, viola1_elio, viola2_elio]

    # Colori argon

    rosso_argon = np.mean ([912.3, 965.8])
    giallo_argon = np.mean ([750.4, 763.5, 794.8, 800.6, 801.5, 810.4, 811.5])
    verde_argon = np.mean ([696.5, 706.7])
    blu_argon = np.mean ([434.8, 461.0, 488.0, 472.7, 476.7, 480.6, 487.9])
    blu1_argon = 451.1 # più intenso, OK
    blu2_argon = 452.2
    viola1_argon = 404.4
    viola2_argon = 415.9 # più intenso, OK

    colors_argon_p = [rosso_argon, giallo_argon, verde_argon, blu_argon]
    colors_argon_r = [giallo_argon, verde_argon, blu1_argon, blu2_argon, viola1_argon, viola2_argon]

    # Colori neon

    rosso_neon = np.mean ([603, 607.4, 614.3, 616.4, 621.7, 626.7, 638.3, 640.2, 650.7, 660, 693, 703.2, 717.4, 724.5])
    giallo_neon = 585.3
    verde_neon = np.mean ([501.6, 540.1])
    blu1_neon = 450.1 # più intenso, OK
    blu2_neon = 451.0
    viola1_neon = 403.8
    viola2_neon = 404.3 # più intenso, OK

    colors_neon_p = [rosso_neon, giallo_neon, verde_neon, blu1_neon]
    colors_neon_r = [giallo_neon, verde_neon, blu1_neon, blu2_neon, viola1_neon, viola2_neon]

    # Colori Kripton

    rosso__kripton = np.mean ([642.0, 729, 740.7, 760.2])
    giallo_kripton = 0
    verde_kripton = np.mean ([557, 587.1])
    blu1_kripton = 450.2 # più intenso, OK
    blu2_kripton = 455.0
    blu_kripton = np.mean ([435.6, 461.9, 465.9, 473.9, 476.6, 483.2, 484.7])
    viola1_kripton = 332.0
    viola2_kripton = 337.6

    colors_kripton_p = [rosso__kripton, giallo_kripton, verde_kripton, blu_kripton]
    colors_kripton_r = [giallo_kripton, verde_kripton, blu1_kripton, blu2_kripton, viola1_kripton, viola2_kripton]

    # Colori Xenon

    rosso_xenon = 699.1
    giallo_xenon = np.mean ([597.7, 605.1, 609.8])
    verde_xenon = np.mean ([529.2, 541.9])
    blu1_xenon = 473.4 # più intenso, OK
    blu2_xenon = 480.7
    viola1_xenon = 396.8
    viola2_xenon = 407.9

    colors_xenon_p = [rosso_xenon, giallo_xenon, verde_xenon, blu1_xenon]
    colors_xenon_r = [giallo_xenon, verde_xenon, blu1_xenon, blu2_xenon, viola1_xenon, viola2_xenon]

    # Colori co2

    rosso_co2 = 0
    giallo_co2 = 0
    verde_co2 = 0
    blu_co2 = 0
    viola_co2 = 0

    colors_co2_p = [rosso_co2, giallo_co2, verde_co2, blu_co2]
    colors_co2_r = [giallo_co2, verde_co2, blu_co2, viola_co2]


    # Confronto con elio
    chi_quadro_elio_p, dof_elio_p, p_value_elio_p = compare (colors_elio_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con elio (prisma): chi^2 = {chi_quadro_elio_p:.2f}, dof = {dof_elio_p}, p-value = {p_value_elio_p:.4f}")
    chi_quadro_elio_r, dof_elio_r, p_value_elio_r = compare (colors_elio_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con elio (reticolo): chi^2 = {chi_quadro_elio_r:.2f}, dof = {dof_elio_r}, p-value = {p_value_elio_r:.4f}\n")

    # Confronto con argon
    chi_quadro_argon_p, dof_argon_p, p_value_argon_p = compare (colors_argon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con argon (prisma): chi^2 = {chi_quadro_argon_p:.2f}, dof = {dof_argon_p}, p-value = {p_value_argon_p:.4f}")
    chi_quadro_argon_r, dof_argon_r, p_value_argon_r = compare (colors_argon_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con argon (reticolo): chi^2 = {chi_quadro_argon_r:.2f}, dof = {dof_argon_r}, p-value = {p_value_argon_r:.4f}\n")

    # Confronto con neon   
    chi_quadro_neon_p, dof_neon_p, p_value_neon_p = compare (colors_neon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con neon (prisma): chi^2 = {chi_quadro_neon_p:.2f}, dof = {dof_neon_p}, p-value = {p_value_neon_p:.4f}")
    chi_quadro_neon_r, dof_neon_r, p_value_neon_r = compare (colors_neon_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con neon (reticolo): chi^2 = {chi_quadro_neon_r:.2f}, dof = {dof_neon_r}, p-value = {p_value_neon_r:.4f}\n")

    # Confronto con kripton
    chi_quadro_kripton_p, dof_kripton_p, p_value_kripton_p = compare (colors_kripton_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con kripton (prisma): chi^2 = {chi_quadro_kripton_p:.2f}, dof = {dof_kripton_p}, p-value = {p_value_kripton_p:.4f}")
    chi_quadro_kripton_r, dof_kripton_r, p_value_kripton_r = compare (colors_kripton_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con kripton (reticolo): chi^2 = {chi_quadro_kripton_r:.2f}, dof = {dof_kripton_r}, p-value = {p_value_kripton_r:.4f}\n")
    
    # Confronto con xenon
    chi_quadro_xenon_p, dof_xenon_p, p_value_xenon_p = compare (colors_xenon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con xenon (prisma): chi^2 = {chi_quadro_xenon_p:.2f}, dof = {dof_xenon_p}, p-value = {p_value_xenon_p:.4f}")
    chi_quadro_xenon_r, dof_xenon_r, p_value_xenon_r = compare (colors_xenon_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con xenon (reticolo): chi^2 = {chi_quadro_xenon_r:.2f}, dof = {dof_xenon_r}, p-value = {p_value_xenon_r:.4f}\n")

    # Confronto con co2
    chi_quadro_co2_p, dof_co2_p, p_value_co2_p = compare (colors_co2_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con CO2 (prisma): chi^2 = {chi_quadro_co2_p:.2f}, dof = {dof_co2_p}, p-value = {p_value_co2_p:.4f}")
    chi_quadro_co2_r, dof_co2_r, p_value_co2_r = compare (colors_co2_r, colors_ignoto_r, colors_ignoto_sigma_r)
    print (f"Confronto con CO2 (reticolo): chi^2 = {chi_quadro_co2_r:.2f}, dof = {dof_co2_r}, p-value = {p_value_co2_r:.4f}\n")