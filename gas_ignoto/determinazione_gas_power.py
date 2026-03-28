import numpy as np
from scipy.optimize import linear_sum_assignment


# Dati sperimentali dell'ignoto
OBSERVED_DATA = {
    "prisma": {
        "labels": ["rosso", "giallo", "verde", "blu"],
        "wavelengths": np.array([780.5115, 677.5714, 603.7090, 451.7410]),
        "sigma": np.array([335.8858, 225.9965, 169.9630, 92.0307]),
    },
    "reticolo": {
        "labels": ["giallo", "verde", "blu1", "blu2", "viola1", "viola2"],
        "wavelengths": np.array([576.448, 550.037, 438.351, 437.833, 397.412, 401.237]),
        "sigma": np.array([28.137, 30.003, 30.790, 32.882, 36.704, 37.473]),
    },
}


# Linee teoriche candidate.
# Ho tenuto liste abbastanza compatte per evitare che il matching si faccia "aiutare"
# da troppe linee lontane o secondarie.
GASES = {
    "Elio": {
        "prisma": [447.1, 501.6, 587.6, 667.8, 706.5, 728.1],
        "reticolo": [388.9, 402.6, 447.1, 501.6, 587.6, 667.8, 706.5, 728.1],
    },
    "Argon": {
        "prisma": [434.8, 451.1, 461.0, 472.7, 488.0, 696.5, 706.7, 750.4, 763.5, 794.8, 800.6, 811.5],
        "reticolo": [404.4, 415.9, 434.8, 451.1, 452.2, 461.0, 472.7, 488.0, 696.5, 706.7],
    },
    "Neon": {
        "prisma": [450.1, 451.0, 501.6, 540.1, 585.3, 603.0, 607.4, 614.3, 616.4, 621.7, 626.7, 638.3, 640.2, 650.7, 660.0, 693.0, 703.2, 717.4, 724.5],
        "reticolo": [403.8, 404.3, 450.1, 451.0, 540.1, 585.3],
    },
    "Kripton": {
        "prisma": [435.6, 450.2, 455.0, 461.9, 473.9, 483.2, 557.0, 587.1, 642.0, 729.0, 740.7, 760.2],
        "reticolo": [332.0, 337.6, 435.6, 450.2, 455.0, 461.9, 473.9, 483.2, 557.0, 587.1],
    },
    "Xenon": {
        "prisma": [396.8, 407.9, 473.4, 480.7, 529.2, 541.9, 597.7, 605.1, 609.8, 699.1],
        "reticolo": [396.8, 407.9, 473.4, 480.7, 529.2, 541.9, 597.7, 605.1, 609.8, 699.1],
    },
    "CO2": {
        "prisma": [],
        "reticolo": [],
    },
}


def chi2_distance(observed, theory, sigma):
    return float(np.sum(((observed - theory) / sigma) ** 2))


def best_unique_match(observed, sigma, theory_lines):
    """
    Cerca il matching 1-a-1 che minimizza il chi^2.
    Ogni riga teorica puo' essere usata al piu' una volta.
    """
    observed = np.asarray(observed, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
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

    cost_matrix = ((observed[:, None] - theory_lines[None, :]) / sigma[:, None]) ** 2
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


def rank_gases(dataset_name, observed, sigma):
    results = []
    for gas_name, gas_data in GASES.items():
        match = best_unique_match(observed, sigma, gas_data[dataset_name])
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
        ranking = rank_gases(dataset_name, dataset["wavelengths"], dataset["sigma"])
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
    for gas_name in GASES:
        total = 0.0
        for dataset_name, payload in sample_by_dataset.items():
            match = best_unique_match(payload["wavelengths"], payload["sigma"], GASES[gas_name][dataset_name])
            total += match["chi2"]
        scores[gas_name] = total
    best_gas = min(scores, key=scores.get)
    return best_gas, scores


def monte_carlo_power(n_sim=5000, seed=12345):
    rng = np.random.default_rng(seed)
    templates = {}

    # Usiamo il matching migliore sui dati reali come "template" delle righe attese.
    for dataset_name, dataset in OBSERVED_DATA.items():
        templates[dataset_name] = {}
        ranking = rank_gases(dataset_name, dataset["wavelengths"], dataset["sigma"])
        for item in ranking:
            templates[dataset_name][item["gas"]] = item["matched_lines"]

    gas_names = list(GASES.keys())
    confusion = {true_gas: {pred_gas: 0 for pred_gas in gas_names} for true_gas in gas_names}

    for true_gas in gas_names:
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
    for gas_name in gas_names:
        total = sum(confusion[gas_name].values())
        power[gas_name] = confusion[gas_name][gas_name] / total if total > 0 else np.nan

    return power, confusion


def print_dataset_report(dataset_name):
    dataset = OBSERVED_DATA[dataset_name]
    ranking = rank_gases(dataset_name, dataset["wavelengths"], dataset["sigma"])

    print(f"\n=== RISULTATI {dataset_name.upper()} ===")
    print(f"Righe osservate: {np.round(dataset['wavelengths'], 3)} nm")
    print(f"Incertezze     : {np.round(dataset['sigma'], 3)} nm\n")

    for item in ranking:
        matched = np.round(item["matched_lines"], 3)
        chi2_val = item["chi2"]
        red = item["reduced_chi2"]
        print(
            f"{item['gas']:8s}  chi^2 = {chi2_val:9.3f}   "
            f"chi^2_rid = {red:8.3f}   match = {matched}"
        )

    if len(ranking) >= 2:
        delta = ranking[1]["chi2"] - ranking[0]["chi2"]
        print(f"\nMiglior candidato {dataset_name}: {ranking[0]['gas']}  (delta chi^2 = {delta:.3f})")


def print_combined_report():
    combined = combined_ranking()

    print("\n=== RISULTATI COMBINATI PRISMA + RETICOLO ===\n")
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


def print_power_report(n_sim=5000, seed=12345):
    power, confusion = monte_carlo_power(n_sim=n_sim, seed=seed)
    gas_names = list(GASES.keys())

    print("\n=== POWER TEST MONTE CARLO ===")
    print(f"Numero simulazioni per gas: {n_sim}\n")

    for gas_name in gas_names:
        value = power[gas_name]
        if np.isnan(value):
            print(f"{gas_name:8s}  power = non definita")
        else:
            print(f"{gas_name:8s}  power = {value:.4f}")

    print("\nMatrice di confusione (righe = gas vero, colonne = gas stimato):\n")
    header = " " * 10 + "".join(f"{name:>10s}" for name in gas_names)
    print(header)
    for true_gas in gas_names:
        row = f"{true_gas:10s}" + "".join(f"{confusion[true_gas][pred_gas]:10d}" for pred_gas in gas_names)
        print(row)


def main():
    print_dataset_report("prisma")
    print_dataset_report("reticolo")
    print_combined_report()
    print_power_report(n_sim=3000, seed=12345)


if __name__ == "__main__":
    main()
