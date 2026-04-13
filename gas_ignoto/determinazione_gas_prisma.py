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

    # Con prisma, abbiamo ottenuto i seguenti valori di λ (con relative deviazioni standard):

    rosso_ignoto_p = 780.5115 # sus... oltre lo spettro visibile...
    sigma_rosso_ignoto_p = 335.8858
    giallo_ignoto_p = 677.5714 # sus... nel rosso
    sigma_giallo_ignoto_p = 225.9965
    verde_ignoto_p = 603.7090 # sus... nel giallo
    sigma_verde_ignoto_p = 169.9630
    blu_ignoto_p = 451.7410 # ok, nel blu
    sigma_blu_ignoto_p = 92.0307


    # Procediamo al confronto con gas nobili e co2, usando i valori di λ ottenuti con il prisma (con relative deviazioni standard):

    colors_p = ["rosso", "giallo", "verde", "blu"]
    colors_ignoto_p = [rosso_ignoto_p, giallo_ignoto_p, verde_ignoto_p, blu_ignoto_p]
    colors_ignoto_sigma_p = [sigma_rosso_ignoto_p, sigma_giallo_ignoto_p, sigma_verde_ignoto_p, sigma_blu_ignoto_p]


    # Colori elio

    rosso_elio = np.mean ([706.5, 728.1])
    print (f"Rosso elio: {rosso_elio:.1f} nm")  
    giallo_elio = np.mean ([587.6, 667.8])
    print (f"Giallo elio: {giallo_elio:.1f} nm")
    verde_elio = 501.6
    print (f"Verde elio: {verde_elio:.1f} nm")
    blu_elio = 447.1
    print (f"Blu elio: {blu_elio:.1f} nm")  

    colors_elio_p = [rosso_elio, giallo_elio, verde_elio, blu_elio]
 

    # Colori argon

    rosso_argon = np.mean ([912.3, 965.8])
    print (f"Rosso argon: {rosso_argon:.1f} nm")
    giallo_argon = np.mean ([750.4, 763.5, 794.8, 800.6, 801.5, 810.4, 811.5])
    print (f"Giallo argon: {giallo_argon:.1f} nm")
    verde_argon = np.mean ([696.5, 706.7])
    print (f"Verde argon: {verde_argon:.1f} nm")
    blu_argon = np.mean ([434.8, 461.0, 488.0, 472.7, 476.7, 480.6, 487.9])
    print (f"Blu argon: {blu_argon:.1f} nm")

    colors_argon_p = [rosso_argon, giallo_argon, verde_argon, blu_argon]


    # Colori neon

    rosso_neon = np.mean ([603, 607.4, 614.3, 616.4, 621.7, 626.7, 638.3, 640.2, 650.7, 660, 693, 703.2, 717.4, 724.5])
    print (f"Rosso neon: {rosso_neon:.1f} nm")
    giallo_neon = 585.3
    print (f"Giallo neon: {giallo_neon:.1f} nm")
    verde_neon = np.mean ([501.6, 540.1])
    print (f"Verde neon: {verde_neon:.1f} nm")
    blu_neon = 450.1 
    print (f"Blu neon: {blu_neon:.1f} nm")

    colors_neon_p = [rosso_neon, giallo_neon, verde_neon, blu_neon]


    # Colori Kripton

    rosso__kripton = np.mean ([642.0, 729, 740.7, 760.2])
    print (f"Rosso kripton: {rosso__kripton:.1f} nm")
    giallo_kripton = 0
    print (f"Giallo kripton: {giallo_kripton:.1f} nm")
    verde_kripton = np.mean ([557, 587.1])
    print (f"Verde kripton: {verde_kripton:.1f} nm")
    blu_kripton = np.mean ([435.6, 461.9, 465.9, 473.9, 476.6, 483.2, 484.7])
    print (f"Blu kripton: {blu_kripton:.1f} nm")

    colors_kripton_p = [rosso__kripton, giallo_kripton, verde_kripton, blu_kripton]
    

    # Colori Xenon

    rosso_xenon = 699.1
    print (f"Rosso xenon: {rosso_xenon:.1f} nm")
    giallo_xenon = np.mean ([597.7, 605.1, 609.8])
    print (f"Giallo xenon: {giallo_xenon:.1f} nm")
    verde_xenon = np.mean ([529.2, 541.9])
    print (f"Verde xenon: {verde_xenon:.1f} nm")
    blu_xenon = 473.4 # più intenso, OK
    print (f"Blu xenon: {blu_xenon:.1f} nm")

    colors_xenon_p = [rosso_xenon, giallo_xenon, verde_xenon, blu_xenon]
    
    #Co2

    rosso_co2 = 0
    print (f"Rosso CO2: {rosso_co2:.1f} nm")
    giallo_co2 = 0
    print (f"Giallo CO2: {giallo_co2:.1f} nm")
    verde_co2 = 0
    print (f"Verde CO2: {verde_co2:.1f} nm")
    blu_co2 = 0
    print (f"Blu CO2: {blu_co2:.1f} nm")
    viola_co2 = 0
    print (f"Viola CO2: {viola_co2:.1f} nm")

    colors_co2_p = [rosso_co2, giallo_co2, verde_co2, blu_co2]



    # Confronto con elio
    chi_quadro_elio_p, dof_elio_p, p_value_elio_p = compare (colors_elio_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con elio (prisma): chi^2 = {chi_quadro_elio_p:.2f}, dof = {dof_elio_p}, p-value = {p_value_elio_p:.4f}")


    # Confronto con argon
    chi_quadro_argon_p, dof_argon_p, p_value_argon_p = compare (colors_argon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con argon (prisma): chi^2 = {chi_quadro_argon_p:.2f}, dof = {dof_argon_p}, p-value = {p_value_argon_p:.4f}")


    # Confronto con neon   
    chi_quadro_neon_p, dof_neon_p, p_value_neon_p = compare (colors_neon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con neon (prisma): chi^2 = {chi_quadro_neon_p:.2f}, dof = {dof_neon_p}, p-value = {p_value_neon_p:.4f}")
   

    # Confronto con kripton
    chi_quadro_kripton_p, dof_kripton_p, p_value_kripton_p = compare (colors_kripton_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con kripton (prisma): chi^2 = {chi_quadro_kripton_p:.2f}, dof = {dof_kripton_p}, p-value = {p_value_kripton_p:.4f}")

    
    # Confronto con xenon
    chi_quadro_xenon_p, dof_xenon_p, p_value_xenon_p = compare (colors_xenon_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con xenon (prisma): chi^2 = {chi_quadro_xenon_p:.2f}, dof = {dof_xenon_p}, p-value = {p_value_xenon_p:.4f}")
 

    # Confronto con co2
    chi_quadro_co2_p, dof_co2_p, p_value_co2_p = compare (colors_co2_p, colors_ignoto_p, colors_ignoto_sigma_p)
    print (f"Confronto con CO2 (prisma): chi^2 = {chi_quadro_co2_p:.2f}, dof = {dof_co2_p}, p-value = {p_value_co2_p:.4f}")