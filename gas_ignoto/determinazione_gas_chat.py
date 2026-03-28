import numpy as np
from scipy.stats import chi2

# CIAO, SONO VALE
# IL PROGRAMMA L'HA FATTO CHAT... OVVIAMENTE C'è QUALCOSA CHE NON VA, PERCHé TUTTI I CHI QUADRI SONO BELLI..
# MANNAGGIA A TE CHAT...
# DOPO LO CONTROLLO, ORA VADO A MANGIARE, CIAO CIAO

# Funzioni per il confronto

def chi_square (exp, theory, sigma):
    diff = [(e - t)**2 / s**2 for e, t, s in zip (exp, theory, sigma)]
    chi2_val = np.sum (diff)
    dof = len (exp) - 1
    p_value = chi2.sf (chi2_val, dof)
    return chi2_val, dof, p_value

def match_lines (exp_lines, theory_lines):
    matched = []
    for e in exp_lines:
        closest = min (theory_lines, key=lambda t: abs (t - e))
        matched.append (closest)
    return matched

def full_comparison(exp_lines, sigma, label):
    print(f"\n=== Confronto dati {label} ===\n")
    for gas_name, theory_lines in gases.items():
        matched = match_lines(exp_lines, theory_lines)
        chi2_val, dof, p_val = chi_square(exp_lines, matched, sigma)
        print(f"{gas_name}:")
        print(f"  linee teoriche matchate = {np.round(matched,1)}")
        print(f"  chi^2 = {chi2_val:.2f}, dof = {dof}, p-value = {p_val:.4f}\n")



if __name__ == "__main__":

    # Dati reticolo
    exp_lines_reticolo = np.array([576.448, 550.037, 438.351, 437.833, 397.412, 401.237])
    sigma_reticolo = np.array([28.137, 30.003, 30.79, 32.882, 36.704, 37.473])

    # Dati prisma
    exp_lines_prisma = np.array([677.5714, 603.7090, 451.7410, 780.5115])
    sigma_prisma = np.array([225.9965, 169.9630, 92.0307, 335.8858])

    # Linee spettrali teoriche dei gas nobili e co2
    gases = {
        "Elio": [587.6, 501.6, 447.1, 402.6, 388.9, 667.8, 706.5, 728.1],
        "Argon": [696.5, 706.7, 451.1, 452.2, 404.4, 415.9],
        "Neon": [585.3, 540.1, 450.1, 451.0, 403.8, 404.3],
        "Kripton": [557, 587.1, 450.2, 455.0, 435.6],
        "Xenon": [597.7, 605.1, 529.2, 541.9, 473.4, 480.7, 396.8, 407.9]
    }

    full_comparison(exp_lines_reticolo, sigma_reticolo, "Reticolo")
    full_comparison(exp_lines_prisma, sigma_prisma, "Prisma")