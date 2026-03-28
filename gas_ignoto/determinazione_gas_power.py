import os
from pathlib import Path

# COMMENTO: (sono vale)

# Ho fatto dei toy experiments misurare il tasso di falsi positivi e falsi negativi:
#   - si suppone reale un gas, e si creano dati fittizi con le righe di quel gas + rumore, 
#     e si vede se il test lo riconosce correttamente
#   - tutti i dati sono poi riportati in tabelle e grafici (dentro gas_ignoto/output_power_test) 
#     che mostrano come il test si comporta al variare di soglia, intensità delle righe, ecc.

# OSS:
#      - Con il reticolo, il gas viene Elio ma anche altri gas hanno compatibilità notevole, soprattutto lo Xenon
#      - Il power test mostra che spesso, se il gas reale è Elio, lo spettro mostra corrispondenze 
#        con quello dello Xenon (ciò potrebbe spiegare come mai lo Xenon ha un valore di matching così alto)

# per commento più approfondito su ogni gas, vedere il documento latex :))


LOCAL_MPL_DIR = Path(__file__).resolve().parent / ".mplconfig"
LOCAL_MPL_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_MPL_DIR))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment


OUTPUT_DIR = Path(__file__).resolve().parent / "output_power_test"
N_MONTE_CARLO = 3000
RNG_SEED = 12345


# Dati sperimentali dell'ignoto
OBSERVED_DATA = {
    "prisma": {
        "labels": ["rosso", "giallo", "verde", "blu"],
        "wavelengths": np.array([780.5115, 677.5714, 603.7090, 451.7410]),
        "sigma": np.array([335.8858, 225.9965, 169.9630, 92.0307]),
        "weights": np.array([0.35, 1.60, 1.00, 1.10]),
        "notes": "Rosso molto debole e poco separato: peso ridotto. Giallo molto intenso: peso aumentato.",
    },
    "reticolo": {
        "labels": ["giallo", "verde", "blu1", "blu2", "viola1", "viola2"],
        "wavelengths": np.array([576.522, 550.105, 438.405, 437.888, 397.461, 401.287]),
        "sigma": np.array([28.140, 30.007, 30.794, 32.887, 36.709, 37.478]),
        "weights": np.array([1.50, 0.75, 1.00, 0.90, 1.00, 1.05]),
        "notes": "Giallo piu' affidabile; la riga verde vicino a 550 nm e' sospetta e viene pesata meno.",
    },
}


# Le linee sono prese da NIST ASD (Atomic Spectra Database) e filtrate per intensità relativa
GAS_LIBRARY = {
    "Elio": {
        "source": "NIST ASD, righe visibili piu' intense usate in laboratorio",
        "notes": "Se vuoi forzare di piu' l'ipotesi Elio, qui conviene inserire solo le transizioni davvero osservabili nel setup.",
        "min_relative_intensity": {
            "prisma": 0.18,
            "reticolo": 0.12,
        },
        "lines": {
            "prisma": [
                {"wavelength": 447.1, "intensity": 0.32},
                {"wavelength": 501.6, "intensity": 0.24},
                {"wavelength": 587.6, "intensity": 1.00},
                {"wavelength": 667.8, "intensity": 0.40},
                {"wavelength": 706.5, "intensity": 0.72},
                {"wavelength": 728.1, "intensity": 0.22},
            ],
            "reticolo": [
                {"wavelength": 388.9, "intensity": 0.30},
                {"wavelength": 396.5, "intensity": 0.16},
                {"wavelength": 402.6, "intensity": 0.34},
                {"wavelength": 447.1, "intensity": 0.32},
                {"wavelength": 471.3, "intensity": 0.18},
                {"wavelength": 492.2, "intensity": 0.16},
                {"wavelength": 501.6, "intensity": 0.24},
                {"wavelength": 587.6, "intensity": 1.00},
                {"wavelength": 667.8, "intensity": 0.40},
                {"wavelength": 706.5, "intensity": 0.72},
                {"wavelength": 728.1, "intensity": 0.22},
            ],
        },
    },
    "Argon": {
        "source": "NIST ASD, sottoinsieme di righe nel visibile",
        "notes": "Lista volutamente contenuta per evitare matching troppo facili con righe deboli o lontane.",
        "min_relative_intensity": {
            "prisma": 0.25,
            "reticolo": 0.22,
        },
        "lines": {
            "prisma": [
                {"wavelength": 434.8, "intensity": 0.35},
                {"wavelength": 451.1, "intensity": 0.50},
                {"wavelength": 461.0, "intensity": 0.32},
                {"wavelength": 472.7, "intensity": 0.24},
                {"wavelength": 488.0, "intensity": 0.22},
                {"wavelength": 696.5, "intensity": 0.78},
                {"wavelength": 706.7, "intensity": 0.74},
                {"wavelength": 750.4, "intensity": 0.52},
                {"wavelength": 763.5, "intensity": 0.46},
                {"wavelength": 794.8, "intensity": 0.44},
                {"wavelength": 800.6, "intensity": 0.40},
                {"wavelength": 811.5, "intensity": 0.42},
            ],
            "reticolo": [
                {"wavelength": 404.4, "intensity": 0.28},
                {"wavelength": 415.9, "intensity": 0.24},
                {"wavelength": 434.8, "intensity": 0.35},
                {"wavelength": 451.1, "intensity": 0.50},
                {"wavelength": 452.2, "intensity": 0.30},
                {"wavelength": 461.0, "intensity": 0.32},
                {"wavelength": 472.7, "intensity": 0.24},
                {"wavelength": 488.0, "intensity": 0.22},
                {"wavelength": 696.5, "intensity": 0.78},
                {"wavelength": 706.7, "intensity": 0.74},
            ],
        },
    },
    "Neon": {
        "source": "NIST ASD, righe intense nel visibile",
        "notes": "Neon tende a vincere facilmente se gli si lascia molte righe rosse e arancioni vicine alle lambda misurate.",
        "min_relative_intensity": {
            "prisma": 0.42,
            "reticolo": 0.40,
        },
        "lines": {
            "prisma": [
                {"wavelength": 450.1, "intensity": 0.30},
                {"wavelength": 451.0, "intensity": 0.28},
                {"wavelength": 501.6, "intensity": 0.18},
                {"wavelength": 540.1, "intensity": 0.48},
                {"wavelength": 585.3, "intensity": 1.00},
                {"wavelength": 603.0, "intensity": 0.62},
                {"wavelength": 607.4, "intensity": 0.58},
                {"wavelength": 614.3, "intensity": 0.55},
                {"wavelength": 616.4, "intensity": 0.54},
                {"wavelength": 621.7, "intensity": 0.52},
                {"wavelength": 626.7, "intensity": 0.50},
                {"wavelength": 638.3, "intensity": 0.44},
                {"wavelength": 640.2, "intensity": 0.45},
                {"wavelength": 650.7, "intensity": 0.47},
                {"wavelength": 660.0, "intensity": 0.60},
                {"wavelength": 693.0, "intensity": 0.70},
                {"wavelength": 703.2, "intensity": 0.68},
                {"wavelength": 717.4, "intensity": 0.66},
                {"wavelength": 724.5, "intensity": 0.64},
            ],
            "reticolo": [
                {"wavelength": 403.8, "intensity": 0.44},
                {"wavelength": 404.3, "intensity": 0.42},
                {"wavelength": 450.1, "intensity": 0.30},
                {"wavelength": 451.0, "intensity": 0.28},
                {"wavelength": 540.1, "intensity": 0.48},
                {"wavelength": 585.3, "intensity": 1.00},
            ],
        },
    },
    "Kripton": {
        "source": "NIST ASD, righe nel blu-verde-rosso usate per confronto",
        "notes": "Anche qui si potrebbe restringere ulteriormente per un test piu' conservativo.",
        "min_relative_intensity": {
            "prisma": 0.26,
            "reticolo": 0.24,
        },
        "lines": {
            "prisma": [
                {"wavelength": 435.6, "intensity": 0.36},
                {"wavelength": 450.2, "intensity": 0.40},
                {"wavelength": 455.0, "intensity": 0.31},
                {"wavelength": 461.9, "intensity": 0.28},
                {"wavelength": 473.9, "intensity": 0.26},
                {"wavelength": 483.2, "intensity": 0.24},
                {"wavelength": 557.0, "intensity": 0.48},
                {"wavelength": 587.1, "intensity": 0.58},
                {"wavelength": 642.0, "intensity": 0.34},
                {"wavelength": 729.0, "intensity": 0.62},
                {"wavelength": 740.7, "intensity": 0.56},
                {"wavelength": 760.2, "intensity": 0.60},
            ],
            "reticolo": [
                {"wavelength": 332.0, "intensity": 0.24},
                {"wavelength": 337.6, "intensity": 0.25},
                {"wavelength": 435.6, "intensity": 0.36},
                {"wavelength": 450.2, "intensity": 0.40},
                {"wavelength": 455.0, "intensity": 0.31},
                {"wavelength": 461.9, "intensity": 0.28},
                {"wavelength": 473.9, "intensity": 0.26},
                {"wavelength": 483.2, "intensity": 0.24},
                {"wavelength": 557.0, "intensity": 0.48},
                {"wavelength": 587.1, "intensity": 0.58},
            ],
        },
    },
    "Xenon": {
        "source": "NIST ASD, righe nel visibile",
        "notes": "Xenon qui e' tenuto come set compatto per non renderlo troppo permissivo.",
        "min_relative_intensity": {
            "prisma": 0.30,
            "reticolo": 0.30,
        },
        "lines": {
            "prisma": [
                {"wavelength": 396.8, "intensity": 0.42},
                {"wavelength": 407.9, "intensity": 0.38},
                {"wavelength": 473.4, "intensity": 0.34},
                {"wavelength": 480.7, "intensity": 0.32},
                {"wavelength": 529.2, "intensity": 0.36},
                {"wavelength": 541.9, "intensity": 0.40},
                {"wavelength": 597.7, "intensity": 0.58},
                {"wavelength": 605.1, "intensity": 0.54},
                {"wavelength": 609.8, "intensity": 0.50},
                {"wavelength": 699.1, "intensity": 0.48},
            ],
            "reticolo": [
                {"wavelength": 396.8, "intensity": 0.42},
                {"wavelength": 407.9, "intensity": 0.38},
                {"wavelength": 473.4, "intensity": 0.34},
                {"wavelength": 480.7, "intensity": 0.32},
                {"wavelength": 529.2, "intensity": 0.36},
                {"wavelength": 541.9, "intensity": 0.40},
                {"wavelength": 597.7, "intensity": 0.58},
                {"wavelength": 605.1, "intensity": 0.54},
                {"wavelength": 609.8, "intensity": 0.50},
                {"wavelength": 699.1, "intensity": 0.48},
            ],
        },
    },
    "CO2": {
        "source": "Nessuna riga atomica visibile trattata in questo modello semplificato",
        "notes": "CO2 resta come controllo negativo.",
        "min_relative_intensity": {
            "prisma": 1.0,
            "reticolo": 1.0,
        },
        "lines": {
            "prisma": [],
            "reticolo": [],
        },
    },
}


def gas_names():
    return list(GAS_LIBRARY.keys())


def get_line_entries(gas_name, dataset_name):
    return GAS_LIBRARY[gas_name]["lines"][dataset_name]


def get_min_relative_intensity(gas_name, dataset_name):
    return GAS_LIBRARY[gas_name]["min_relative_intensity"][dataset_name]


def get_theory_lines(gas_name, dataset_name):
    entries = get_line_entries(gas_name, dataset_name)
    if len(entries) == 0:
        return []
    min_intensity = get_min_relative_intensity(gas_name, dataset_name)
    return [entry["wavelength"] for entry in entries if entry["intensity"] >= min_intensity]


def get_theory_intensities(gas_name, dataset_name):
    entries = get_line_entries(gas_name, dataset_name)
    if len(entries) == 0:
        return []
    min_intensity = get_min_relative_intensity(gas_name, dataset_name)
    return [entry["intensity"] for entry in entries if entry["intensity"] >= min_intensity]


def effective_sigma(sigma, weights=None):
    sigma = np.asarray(sigma, dtype=float)
    if weights is None:
        return sigma
    weights = np.asarray(weights, dtype=float)
    return sigma / np.sqrt(weights)


def chi2_distance(observed, theory, sigma, weights=None):
    sigma_eff = effective_sigma(sigma, weights)
    return float(np.sum(((observed - theory) / sigma_eff) ** 2))


def best_unique_match(observed, sigma, theory_lines, weights=None):
    
    # Matching 1-a-1 tra righe osservate e teoriche.
    # Ogni riga teorica puo' essere usata al massimo una volta.

    observed = np.asarray(observed, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    sigma_eff = effective_sigma(sigma, weights)
    theory_lines = np.asarray(theory_lines, dtype=float)

    n_obs = len(observed)
    n_theory = len(theory_lines)

    if n_theory == 0:
        return {
            "matched_lines": np.full(n_obs, np.nan),
            "chi2": np.inf,
            "dof": n_obs,
            "reduced_chi2": np.inf,
        }

    if n_theory < n_obs:
        padded = np.concatenate([theory_lines, np.repeat(np.nan, n_obs - n_theory)])
        return {
            "matched_lines": padded[:n_obs],
            "chi2": np.inf,
            "dof": n_obs,
            "reduced_chi2": np.inf,
        }

    cost_matrix = ((observed[:, None] - theory_lines[None, :]) / sigma_eff[:, None]) ** 2
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    best_match = theory_lines[col_ind]
    best_score = float(cost_matrix[row_ind, col_ind].sum())
    dof = max(n_obs - 1, 1)

    return {
        "matched_lines": best_match,
        "chi2": best_score,
        "dof": dof,
        "reduced_chi2": best_score / dof,
    }


def rank_gases(dataset_name, observed, sigma, weights=None):
    results = []
    for gas_name in gas_names():
        match = best_unique_match(observed, sigma, get_theory_lines(gas_name, dataset_name), weights=weights)
        results.append(
            {
                "gas": gas_name,
                "matched_lines": match["matched_lines"],
                "chi2": match["chi2"],
                "dof": match["dof"],
                "reduced_chi2": match["reduced_chi2"],
            }
        )
    results.sort(key=lambda item: item["chi2"])
    return results


def combined_ranking():
    partial = {}

    for dataset_name, dataset in OBSERVED_DATA.items():
        ranking = rank_gases(
            dataset_name,
            dataset["wavelengths"],
            dataset["sigma"],
            weights=dataset.get("weights"),
        )
        for item in ranking:
            gas = item["gas"]
            partial.setdefault(
                gas,
                {
                    "gas": gas,
                    "chi2_tot": 0.0,
                    "dof_tot": 0,
                    "details": {},
                },
            )
            partial[gas]["chi2_tot"] += item["chi2"]
            partial[gas]["dof_tot"] += item["dof"]
            partial[gas]["details"][dataset_name] = item

    combined = []
    for gas, item in partial.items():
        dof_tot = max(item["dof_tot"], 1)
        combined.append(
            {
                "gas": gas,
                "chi2_tot": item["chi2_tot"],
                "dof_tot": dof_tot,
                "reduced_chi2_tot": item["chi2_tot"] / dof_tot,
                "details": item["details"],
            }
        )

    combined.sort(key=lambda item: item["chi2_tot"])
    return combined


def classify_sample(sample_by_dataset):
    scores = {}
    for gas_name in gas_names():
        total = 0.0
        for dataset_name, payload in sample_by_dataset.items():
            match = best_unique_match(
                payload["wavelengths"],
                payload["sigma"],
                get_theory_lines(gas_name, dataset_name),
                weights=payload.get("weights"),
            )
            total += match["chi2"]
        scores[gas_name] = total
    best_gas = min(scores, key=scores.get)
    return best_gas, scores


def build_templates_from_real_data():
    templates = {}
    for dataset_name, dataset in OBSERVED_DATA.items():
        templates[dataset_name] = {}
        ranking = rank_gases(
            dataset_name,
            dataset["wavelengths"],
            dataset["sigma"],
            weights=dataset.get("weights"),
        )
        for item in ranking:
            templates[dataset_name][item["gas"]] = item["matched_lines"]
    return templates


def monte_carlo_power(n_sim=N_MONTE_CARLO, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    templates = build_templates_from_real_data()
    names = gas_names()
    confusion = {true_gas: {pred_gas: 0 for pred_gas in names} for true_gas in names}

    for true_gas in names:
        valid_template = True
        simulated_base = {}

        for dataset_name, dataset in OBSERVED_DATA.items():
            matched_lines = templates[dataset_name][true_gas]
            if np.any(np.isnan(matched_lines)) or np.isinf(np.sum(matched_lines)):
                valid_template = False
                break
            simulated_base[dataset_name] = {
                "wavelengths": matched_lines,
                "sigma": dataset["sigma"],
                "weights": dataset.get("weights"),
            }

        if not valid_template:
            continue

        for _ in range(n_sim):
            sample = {}
            for dataset_name, payload in simulated_base.items():
                sample[dataset_name] = {
                    "wavelengths": payload["wavelengths"] + rng.normal(0.0, payload["sigma"]),
                    "sigma": payload["sigma"],
                }
            predicted_gas, _ = classify_sample(sample)
            confusion[true_gas][predicted_gas] += 1

    power = {}
    for gas_name in names:
        total = sum(confusion[gas_name].values())
        power[gas_name] = confusion[gas_name][gas_name] / total if total > 0 else np.nan

    return power, confusion


def print_nist_library():
    print("=== Libreria Linee Teoriche ===\n")
    for gas_name in gas_names():
        print(f"{gas_name}:")
        print(f"  fonte : {GAS_LIBRARY[gas_name]['source']}")
        print(f"  note  : {GAS_LIBRARY[gas_name]['notes']}")
        for dataset_name in OBSERVED_DATA:
            entries = get_line_entries(gas_name, dataset_name)
            lines = np.array(get_theory_lines(gas_name, dataset_name), dtype=float)
            intensities = np.array(get_theory_intensities(gas_name, dataset_name), dtype=float)
            threshold = get_min_relative_intensity(gas_name, dataset_name)
            if len(entries) == 0:
                print(f"  {dataset_name:8s}: nessuna riga")
            else:
                print(f"  {dataset_name:8s}: soglia intensita' = {threshold:.2f}")
                print(f"  {'':10s}lambda usate = {np.round(lines, 3)}")
                print(f"  {'':10s}intensita'   = {np.round(intensities, 3)}")
        print()


def print_dataset_report(dataset_name):
    dataset = OBSERVED_DATA[dataset_name]
    ranking = rank_gases(
        dataset_name,
        dataset["wavelengths"],
        dataset["sigma"],
        weights=dataset.get("weights"),
    )

    print(f"\n=== Risultati {dataset_name.upper()} ===")
    print(f"Righe osservate: {np.round(dataset['wavelengths'], 3)} nm")
    print(f"Incertezze     : {np.round(dataset['sigma'], 3)} nm\n")
    print(f"Pesi usati     : {np.round(dataset.get('weights', np.ones_like(dataset['sigma'])), 3)}")
    print(f"Note           : {dataset.get('notes', 'nessuna')}\n")

    for item in ranking:
        matched = np.round(item["matched_lines"], 3)
        print(
            f"{item['gas']:8s}  chi^2 = {item['chi2']:9.3f}   "
            f"chi^2_rid = {item['reduced_chi2']:8.3f}   match = {matched}"
        )

    if len(ranking) >= 2:
        delta = ranking[1]["chi2"] - ranking[0]["chi2"]
        print(f"\nMiglior candidato {dataset_name}: {ranking[0]['gas']}  (delta chi^2 = {delta:.3f})")


def print_combined_report():
    combined = combined_ranking()

    print("\n=== RIisultati combinati PRISMA + RETICOLO ===\n")
    for item in combined:
        print(
            f"{item['gas']:8s}  chi^2_tot = {item['chi2_tot']:10.3f}   "
            f"chi^2_rid_tot = {item['reduced_chi2_tot']:8.3f}"
        )

    if len(combined) >= 2:
        best = combined[0]
        second = combined[1]
        delta = second["chi2_tot"] - best["chi2_tot"]
        print(f"\nGas identificato: {best['gas']}")
        print(f"Secondo migliore: {second['gas']}")
        print(f"Separazione totale delta chi^2 = {delta:.3f}")


def print_power_report(power, confusion, n_sim):
    names = gas_names()
    print("\n=== Power Test Monte Carlo ===")
    print(f"Numero simulazioni per gas: {n_sim}\n")

    for gas_name in names:
        value = power[gas_name]
        if np.isnan(value):
            print(f"{gas_name:8s}  power = non definita")
        else:
            print(f"{gas_name:8s}  power = {value:.4f}")

    print("\nMatrice di confusione (righe = gas vero, colonne = gas stimato):\n")
    header = " " * 10 + "".join(f"{name:>10s}" for name in names)
    print(header)
    for true_gas in names:
        row = f"{true_gas:10s}" + "".join(f"{confusion[true_gas][pred_gas]:10d}" for pred_gas in names)
        print(row)


def make_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def save_ranking_plot(dataset_name, ranking):
    make_output_dir()

    gases = [item["gas"] for item in ranking if np.isfinite(item["chi2"])]
    values = [item["chi2"] for item in ranking if np.isfinite(item["chi2"])]

    fig, ax = plt.subplots(figsize=(8, 4.8))

    colors = ["#0077b6" if idx == 0 else "#90be6d" for idx in range(len(gases))]

    ax.bar(gases, values, color=colors, edgecolor="#1f2937")
    ax.set_title(f"Ranking dei gas - {dataset_name}")
    ax.set_ylabel(r"$\chi^2$")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    output_path = OUTPUT_DIR / f"ranking_{dataset_name}.png"
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def save_spectrum_overlay_plot(dataset_name, ranking, top_n=3):
    make_output_dir()

    dataset = OBSERVED_DATA[dataset_name]
    observed = dataset["wavelengths"]
    labels = dataset["labels"]
    weights = dataset.get("weights", np.ones_like(observed))
    top_candidates = [item for item in ranking if np.isfinite(item["chi2"])][:top_n]

    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    ax.vlines(observed, 0, weights, color="#1d3557", linewidth=3, label="osservato")

    for idx, item in enumerate(top_candidates):
        level = 1.3 + 0.45 * idx
        theory = np.array(get_theory_lines(item["gas"], dataset_name), dtype=float)
        theory_intensity = np.array(get_theory_intensities(item["gas"], dataset_name), dtype=float)
        matched = item["matched_lines"]
        if len(theory) > 0:
            height = 0.08 + 0.22 * theory_intensity / np.max(theory_intensity)
            ax.vlines(theory, level - height, level + height, color="#adb5bd", linewidth=1.1, alpha=0.45)
        ax.scatter(matched, np.full_like(matched, level), s=70, marker="|", linewidths=2.2, label=f"match {item['gas']}")

    for x, label, weight in zip(observed, labels, weights):
        ax.text(x, weight + 0.05, label, rotation=90, va="bottom", ha="center", fontsize=8)

    ax.set_title(f"Confronto righe osservate / teoriche - {dataset_name}")
    ax.set_xlabel("Lunghezza d'onda [nm]")
    ax.set_ylabel("peso relativo")
    ax.grid(axis="x", alpha=0.2)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()

    output_path = OUTPUT_DIR / f"spettro_confronto_{dataset_name}.png"
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def save_combined_plot(combined):
    make_output_dir()

    gases = [item["gas"] for item in combined if np.isfinite(item["chi2_tot"])]
    values = [item["chi2_tot"] for item in combined if np.isfinite(item["chi2_tot"])]

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    colors = ["#d62828" if idx == 0 else "#fcbf49" for idx in range(len(gases))]
    ax.bar(gases, values, color=colors, edgecolor="#1f2937")
    ax.set_title("Ranking combinato prisma + reticolo")
    ax.set_ylabel(r"$\chi^2_{tot}$")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    output_path = OUTPUT_DIR / "ranking_combinato.png"
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def save_confusion_matrix_plot(confusion):
    make_output_dir()

    names = gas_names()
    matrix = np.array([[confusion[row][col] for col in names] for row in names], dtype=float)

    row_sums = matrix.sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalized = np.divide(matrix, row_sums, where=row_sums > 0)
    normalized[row_sums[:, 0] == 0] = np.nan

    fig, ax = plt.subplots(figsize=(7.6, 6.1))
    image = ax.imshow(normalized, cmap="YlOrRd", vmin=0.0, vmax=1.0)
    ax.set_title("Matrice di confusione normalizzata")
    ax.set_xticks(np.arange(len(names)), labels=names, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(names)), labels=names)
    ax.set_xlabel("Gas stimato")
    ax.set_ylabel("Gas vero")

    for i in range(len(names)):
        for j in range(len(names)):
            value = normalized[i, j]
            text = "n.d." if np.isnan(value) else f"{value:.2f}"
            ax.text(j, i, text, ha="center", va="center", color="#111827", fontsize=9)

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="Frazione di classificazioni")
    fig.tight_layout()

    output_path = OUTPUT_DIR / "matrice_confusione.png"
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def print_saved_plots(paths):
    print("\n=== GRAFICI SALVATI ===\n")
    for path in paths:
        print(path)


def try_save_plot(plot_function, *args):
    try:
        return plot_function(*args)
    except Exception as exc:
        print(f"[warning] impossibile salvare il grafico con {plot_function.__name__}: {exc}")
        return None


def main():

    print_nist_library()

    plot_paths = []
    for dataset_name in OBSERVED_DATA:
        print_dataset_report(dataset_name)
        ranking = rank_gases(
            dataset_name,
            OBSERVED_DATA[dataset_name]["wavelengths"],
            OBSERVED_DATA[dataset_name]["sigma"],
            weights=OBSERVED_DATA[dataset_name].get("weights"),
        )
        plot_path = try_save_plot(save_ranking_plot, dataset_name, ranking)
        if plot_path is not None:
            plot_paths.append(plot_path)
        plot_path = try_save_plot(save_spectrum_overlay_plot, dataset_name, ranking)
        if plot_path is not None:
            plot_paths.append(plot_path)

    combined = combined_ranking()
    print_combined_report()
    plot_path = try_save_plot(save_combined_plot, combined)
    if plot_path is not None:
        plot_paths.append(plot_path)

    power, confusion = monte_carlo_power(n_sim=N_MONTE_CARLO, seed=RNG_SEED)
    print_power_report(power, confusion, N_MONTE_CARLO)
    plot_path = try_save_plot(save_confusion_matrix_plot, confusion)
    if plot_path is not None:
        plot_paths.append(plot_path)

    print_saved_plots(plot_paths)


if __name__ == "__main__":
    main()
