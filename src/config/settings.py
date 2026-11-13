"""
Project Configuration and Global Settings
Purchase Propensity Model on Dunnhumby The Complete Journey Dataset
"""
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# Base Project Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "sample_data" / "dunnhumby_The-Complete-Journey" / "dunnhumby_The-Complete-Journey CSV"
OUTPUT_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "docs" / "reports"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class DatasetConfig:
    """Settings for raw Dunnhumby dataset files and column mappings."""
    transaction_file: Path = DATA_DIR / "transaction_data.csv"
    product_file: Path = DATA_DIR / "product.csv"
    demographic_file: Path = DATA_DIR / "hh_demographic.csv"
    causal_file: Path = DATA_DIR / "causal_data.csv"
    campaign_desc_file: Path = DATA_DIR / "campaign_desc.csv"
    campaign_table_file: Path = DATA_DIR / "campaign_table.csv"
    coupon_file: Path = DATA_DIR / "coupon.csv"
    coupon_redempt_file: Path = DATA_DIR / "coupon_redempt.csv"

    # Perishable / Fresh food departments (high-velocity purchase triggers)
    perishable_departments: List[str] = field(default_factory=lambda: [
        "PRODUCE", "MEAT", "MEAT-PCKGD", "DELI", "PASTRY", "DAIRY"
    ])


@dataclass
class TimeWindowConfig:
    """Point-in-Time Sliding Window Configuration."""
    # Length of historical observation window in days (W_obs)
    observation_window_days: int = 180

    # Prediction window length in days (Delta_t) - default 14 days
    prediction_window_days: int = 14

    # Temporal Sliding Cutoff Anchors (t_0)
    # Dataset spans Day 1 to Day 711
    # Train Cutoffs: 11 sliding points between Day 200 and 500 (every 30 days)
    train_cutoffs: List[int] = field(default_factory=lambda: [
        200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500
    ])

    # Validation Cutoffs: 3 points between Day 530 and 590
    val_cutoffs: List[int] = field(default_factory=lambda: [
        530, 560, 590
    ])

    # Out-of-Time Test Cutoffs: 2 points near the end (Day 650, 680)
    test_cutoffs: List[int] = field(default_factory=lambda: [
        650, 680
    ])


@dataclass
class ModelConfig:
    """LightGBM and Baseline Model Parameters."""
    random_state: int = 42
    n_estimators: int = 1000
    early_stopping_rounds: int = 50
    learning_rate: float = 0.03
    max_depth: int = 6
    num_leaves: int = 31
    min_child_samples: int = 20
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    scale_pos_weight: float = 1.0


# Default instances
dataset_config = DatasetConfig()
time_config = TimeWindowConfig()
model_config = ModelConfig()
