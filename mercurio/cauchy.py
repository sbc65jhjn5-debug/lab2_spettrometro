import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares


def Cauchy (x, a, b) :
    return a + (b / x**2)

if __name__ == "__main__" :

    n = [1.63597, 1.61930, 1.62064] #blu verde giallo
    sigma_n = [0.004, 0.004, 0.004] #blu verde giallo
    lamb = [435.8328, 546.0735, 576.9598] #blu verde giallo

    #oss: λ_blu/violetto = [365.0153, 365.4836, 366.3279, 404.6563] (violetto); [433.9223, 434.7494, !435.8328!] (blu)
    #     λ_verde = [546.0735]
    #     λ_giallo = [!576.9598!, 579.0663]

    # Fit:
    
    Q2 = LeastSquares (lamb, n, sigma_n, Cauchy)
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

    # Plot:

    x_axis = np.linspace (min (lamb), max (lamb), 200)

    fig, ax = plt.subplots ()
    ax.set_title ('Legge di Cauchy')
    ax.set_xlabel ('$\\lambda$ (nm)')
    ax.set_ylabel ('indice di rifrazione n')

    colors = ['blue', 'lime', 'yellow']
    labels = ['blu', 'verde', 'giallo']

    for lamb_i, n_i, err_i, lab, c in zip (lamb, n, sigma_n, labels, colors) :
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