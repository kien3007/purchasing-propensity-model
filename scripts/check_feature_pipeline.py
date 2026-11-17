import json
import re
from pathlib import Path

def inspect_notebook(nb_path):
    print(f"\n=======================================================")
    print(f"Inspecting: {nb_path.name}")
    print(f"=======================================================")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    print(f"Total cells: {len(nb['cells'])} ({len(md_cells)} markdown, {len(code_cells)} code)")
    
    # Extract headers
    print("\n--- Main Sections ---")
    for idx, c in enumerate(nb["cells"]):
        if c["cell_type"] == "markdown":
            src = "".join(c["source"])
            headers = [line for line in src.split("\n") if line.strip().startswith("#")]
            for h in headers[:2]:
                print(f"  Cell {idx}: {h}")

    # Search for feature definitions, column lists, saves, loads
    print("\n--- Key Code Operations ---")
    for idx, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            # check if defines feature list or columns or saving/loading data
            lines = src.split("\n")
            interesting = []
            for line in lines:
                l_str = line.strip()
                if any(kw in l_str for kw in [
                    "features =", "feature_cols", "FEATURE_COLS", "columns =",
                    "to_parquet", "read_parquet", "to_csv", "read_csv",
                    "PointInTimeFeatureExtractor", "train_test_split",
                    "target_col", "LABEL", "X_train", "X_val", "X_test",
                    "features_df", "feature_matrix"
                ]):
                    if not l_str.startswith("#"):
                        interesting.append(l_str)
            if interesting:
                print(f"  Cell {idx}:")
                for item in interesting[:5]:
                    print(f"    {item[:100]}")

if __name__ == "__main__":
    nb_dir = Path("notebooks")
    for nb in sorted(nb_dir.glob("*.ipynb")):
        inspect_notebook(nb)
