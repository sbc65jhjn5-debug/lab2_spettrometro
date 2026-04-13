import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares


def Cauchy (x, a, b) :
    return a + (b / x**2)

def Cauchy_for_exp(x, a, b):
    x = np.asarray(x, dtype=float)
    return a + b / x**2

def dCauchy_dx(x, b):
    x = np.asarray(x, dtype=float)
    return -2 * b / x**3


def chi2_con_sigma_lamb(a, b, lamb, sigma_lamb, n, sigma_n):
    lamb = np.asarray(lamb, dtype=float)
    sigma_lamb = np.asarray(sigma_lamb, dtype=float)
    n = np.asarray(n, dtype=float)
    sigma_n = np.asarray(sigma_n, dtype=float)

    y_fit = Cauchy_for_exp(lamb, a, b)
    sigma_eff = np.sqrt(sigma_n**2 + (dCauchy_dx(lamb, b) * sigma_lamb)**2)
    return np.sum(((n - y_fit) / sigma_eff)**2)


if __name__ == "__main__" :

    n = np.array([1.63597, 1.61930, 1.62064]) #blu verde giallo
    sigma_n = np.array([0.004, 0.004, 0.004]) #blu verde giallo
    lamb_theoretical = np.array([435.8328, 546.0735, 567.7105]) #blu verde giallo

    # oss: λ_blu/violetto = [365.0153, 365.4836, 366.3279, 404.6563] (violetto); [433.9223, 434.7494, !435.8328!] (blu)
    #     λ_verde = [546.0735]
    #     λ_giallo = [576.9598, !567.7105!, 579.0663]
    # Sito NIST regala gioie 

    lamb_exp = np.array([493.919, 605.436, np.average ([639.424, 644.924], weights = [2.940, 2.716])], dtype=float) #blu verde giallo (con λ_giallo media di quelle misurate con il reticolo)
    lamb_exp_sigma = np.array([7.325, 5.893, np.sqrt (1 / (1/2.940**2 + 1/2.716**2))], dtype=float)

    # Fit - lambda teoriche:
    
    Q2 = LeastSquares (lamb_theoretical, n, sigma_n, Cauchy)
    m = Minuit (Q2,
                a = 1.569,
                b = 5310
               )
    m.migrad ()
    m.hesse ()

    for par, val, err in  zip (m.parameters, m.values, m.errors) :
        print (f'{par} = {val:.3f} +/- {err:.3f}')

    a_fit = m.values['a']
    b_fit = m.values['b']
    err_a = m.errors['a']
    err_b = m.errors['b']

    # Fit - lambda misurate con il reticolo:
    
    chi2 = lambda a, b: chi2_con_sigma_lamb(a, b, lamb_exp, lamb_exp_sigma, n, sigma_n)

    m_misurate = Minuit(chi2, a=1.569, b=5310)
    m_misurate.errordef = Minuit.LEAST_SQUARES

    m_misurate.migrad()
    m_misurate.hesse()

    print("\nFit con lambda misurate:")
    for par, val, err in zip(m_misurate.parameters, m_misurate.values, m_misurate.errors):
        print(f"{par} = {val:.3f} +/- {err:.3f}")

    a_fit_misurate = m_misurate.values["a"]
    b_fit_misurate = m_misurate.values["b"]
    err_a_misurate = m_misurate.errors["a"]
    err_b_misurate = m_misurate.errors["b"]

    # Plot - teoriche:

    x_axis = np.linspace (min (lamb_theoretical), max (lamb_theoretical), 200)

    fig, ax = plt.subplots ()
    ax.set_title ('Legge di Cauchy - fit con le $\\lambda$ teoriche')
    ax.set_xlabel ('$\\lambda$ (nm)')
    ax.set_ylabel ('indice di rifrazione n')

    colors = ['blue', 'lime', 'yellow']
    labels = ['blu', 'verde', 'giallo']

    for lamb_i, n_i, err_i, lab, c in zip (lamb_theoretical, n, sigma_n, labels, colors) :
        ax.errorbar (lamb_i,
                     n_i,
                     yerr = err_i,
                     linestyle = 'None',
                     label = lab,
                     marker = 'o',
                     capsize = 4,
                     color = c
                    ) 

    ax.plot (x_axis,
             [Cauchy (x, a_fit, b_fit) for x in x_axis],
             label = f'$n(\\lambda) = ({a_fit:.3f} ± {err_a:.3f}) + ({b_fit:.0f} ± {err_b:.0f}) / \\lambda^2$',
             color = 'navy'
            )

    plt.legend ()
    plt.show ()

    # Plot - misurate con il reticolo:

    fig, ax = plt.subplots()

    ax.set_title("Legge di Cauchy - fit con le $\\lambda$ misurate con il reticolo")
    ax.set_xlabel("$\\lambda$ (nm)")
    ax.set_ylabel("indice di rifrazione $n$")

    x_axis_misurate = np.linspace(np.min(lamb_exp) - 20, np.max(lamb_exp) + 20, 200)

    for lamb_i, err_lamb_i, n_i, err_n_i, lab, c in zip (lamb_exp, lamb_exp_sigma, n, sigma_n, labels, colors) :
        ax.errorbar (lamb_i,
                     n_i,
                     xerr = err_lamb_i,
                     yerr = err_n_i,
                     linestyle = 'None',
                     label = lab,
                     marker = 'o',
                     capsize = 4,
                     color = c
                    )

    ax.plot(
        x_axis_misurate,
        Cauchy_for_exp(x_axis_misurate, a_fit_misurate, b_fit_misurate),
        label=rf"$n(\lambda)=({a_fit_misurate:.3f}\pm{err_a_misurate:.3f}) + ({b_fit_misurate:.0f}\pm{err_b_misurate:.0f})/\lambda^2$",
        color="crimson",
    )

    plt.legend()
    plt.show()