"""
Execute notebooks/01_eda_and_data_quality.ipynb and save all outputs (plots, tables, prints)
directly into the notebook file so it is fully pre-rendered and publication-ready.
"""
import nbformat
from nbclient import NotebookClient
from pathlib import Path
import time

def run():
    nb_path = Path("notebooks/01_eda_and_data_quality.ipynb")
    print(f"Loading notebook from {nb_path}...")
    nb = nbformat.read(nb_path, as_version=4)

    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    print("Executing notebook cells... (this may take ~30-60 seconds to process 2.6M transactions)")
    start_t = time.time()
    client.execute()
    elapsed = time.time() - start_t
    print(f"Execution completed successfully in {elapsed:.1f}s!")

    print(f"Saving executed notebook to {nb_path}...")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("All cell outputs and plots saved successfully!")

if __name__ == "__main__":
    run()
