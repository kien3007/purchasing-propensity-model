"""
Point-in-Time Temporal Windowing and Label Generation Module
Guarantees zero data leakage across arbitrary observation cutoffs.
"""
import pandas as pd
import numpy as np
from typing import List, Tuple
import logging

from src.config.settings import time_config

logger = logging.getLogger(__name__)


def generate_point_in_time_labels(
    baskets_df: pd.DataFrame,
    cutoff_day: int,
    delta_t: int = time_config.prediction_window_days,
    all_households: List[int] = list(range(1, 2501)),
) -> pd.DataFrame:
    """
    Generate ground-truth binary labels Y for an arbitrary cutoff date t_0.
    
    Y = 1 if household has >= 1 valid basket in (cutoff_day, cutoff_day + delta_t]
    Y = 0 otherwise.
    
    Ensures all 2,500 households are present in the output.
    """
    # Filter baskets strictly in the future prediction window
    future_baskets = baskets_df[
        (baskets_df["DAY"] > cutoff_day) & 
        (baskets_df["DAY"] <= cutoff_day + delta_t)
    ]
    
    # Identify households that made at least 1 trip in the future window
    active_households = set(future_baskets["household_key"].unique())
    
    # Create target dataframe for all households
    labels = pd.DataFrame({"household_key": all_households})
    labels["cutoff_day"] = cutoff_day
    labels["delta_t"] = delta_t
    labels["target"] = labels["household_key"].isin(active_households).astype(int)
    
    pos_rate = labels["target"].mean()
    logger.info(f"Cutoff t_0={cutoff_day:3d} (delta_t={delta_t}d): {labels['target'].sum():,} active households ({pos_rate*100:.2f}% positive rate).")
    
    return labels


def build_multi_cutoff_dataset_labels(
    baskets_df: pd.DataFrame,
    cutoffs: List[int],
    delta_t: int = time_config.prediction_window_days,
) -> pd.DataFrame:
    """
    Generate concatenated labels across multiple sliding cutoff points.
    """
    dfs = [generate_point_in_time_labels(baskets_df, t0, delta_t) for t0 in cutoffs]
    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"Built multi-cutoff label matrix: {len(combined):,} rows across {len(cutoffs)} cutoffs.")
    return combined
