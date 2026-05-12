import json
import numpy as np
from typing import Dict






def load_results(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)






def to_matrix(results: Dict):
    frame_keys = sorted(map(int, results.keys()))
    rocket_keys = sorted(map(int, next(iter(results.values())).keys()))

    matrix = np.zeros((len(frame_keys), len(rocket_keys)))

    for i, f in enumerate(frame_keys):
        for j, r in enumerate(rocket_keys):
            matrix[i, j] = results[str(f)][str(r)]

    return frame_keys, rocket_keys, matrix






def compute_global_stats(matrix: np.ndarray):

    return {
        "mean_score": float(np.mean(matrix)),
        "std_score": float(np.std(matrix)),
        "min_score": float(np.min(matrix)),
        "max_score": float(np.max(matrix)),
    }






def find_best_config(matrix, frames, rockets):

    i, j = np.unravel_index(np.argmax(matrix), matrix.shape)

    return {
        "best_score": float(matrix[i, j]),
        "best_frame_count": int(frames[i]),
        "best_rocket_count": int(rockets[j]),
        "position": (i, j),
    }






def sensitivity_analysis(matrix, frames, rockets):

    frame_effect = matrix.mean(axis=1)
    rocket_effect = matrix.mean(axis=0)

    return {
        "frame_importance": frame_effect.tolist(),
        "rocket_importance": rocket_effect.tolist(),
        "best_frame_index": int(np.argmax(frame_effect)),
        "best_rocket_index": int(np.argmax(rocket_effect)),
    }






def top_k_configs(matrix, frames, rockets, k=5):

    flat = matrix.flatten()
    indices = np.argsort(flat)[::-1][:k]

    results = []

    for idx in indices:
        i, j = np.unravel_index(idx, matrix.shape)

        results.append({
            "score": float(matrix[i, j]),
            "frame_count": int(frames[i]),
            "rocket_count": int(rockets[j]),
        })

    return results






def optimal_region(matrix):

    threshold = np.percentile(matrix, 90)

    mask = matrix >= threshold

    coords = np.argwhere(mask)

    return {
        "threshold": float(threshold),
        "num_good_points": int(len(coords)),
        "region_coords": coords.tolist(),
    }






def analyze(path: str):

    results = load_results(path)
    frames, rockets, matrix = to_matrix(results)

    analysis = {}

    analysis["global_stats"] = compute_global_stats(matrix)
    analysis["best_config"] = find_best_config(matrix, frames, rockets)
    analysis["sensitivity"] = sensitivity_analysis(matrix, frames, rockets)
    analysis["top_5"] = top_k_configs(matrix, frames, rockets, k=5)
    analysis["optimal_region"] = optimal_region(matrix)

    return analysis






if __name__ == "__main__":

    analysis = analyze("experiment_results.json")

    print("\n=== GLOBAL STATS ===")
    print(analysis["global_stats"])

    print("\n=== BEST CONFIG ===")
    print(analysis["best_config"])

    print("\n=== TOP 5 CONFIGS ===")
    for c in analysis["top_5"]:
        print(c)

    print("\n=== OPTIMAL REGION INFO ===")
    print(analysis["optimal_region"])
