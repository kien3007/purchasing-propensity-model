"""
Execute all notebooks in notebooks/ (01 to 05) and save all outputs (plots, tables, prints)
directly into the notebook files so they are 100% pre-rendered and publication-ready.
"""
import nbformat
from nbclient import NotebookClient
from pathlib import Path
import time
import sys

NOTEBOOKS = [
    "01_eda_and_data_quality.ipynb",
    "02_point_in_time_feature_engineering.ipynb",
    "03_model_training_and_benchmarking.ipynb",
    "04_business_impact_and_decile_lift.ipynb",
    "05_model_explainability_and_shap.ipynb",
]

def run():
    total_start = time.time()
    for nb_name in NOTEBOOKS:
        nb_path = Path("notebooks") / nb_name
        print(f"\n=======================================================")
        print(f"Executing {nb_name}...")
        print(f"=======================================================")
        nb = nbformat.read(nb_path, as_version=4)

        client = NotebookClient(nb, timeout=600, kernel_name="python3")
        start_t = time.time()
        client.execute()
        elapsed = time.time() - start_t
        print(f"Execution of {nb_name} completed in {elapsed:.1f}s!")

        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Saved executed outputs to {nb_path}.")

    total_elapsed = time.time() - total_start
    print(f"\nAll 5 notebooks executed and saved successfully in {total_elapsed:.1f}s!")

if __name__ == "__main__":
    run()
