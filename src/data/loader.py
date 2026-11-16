"""
High-Performance Data Ingestion and Cleansing Module
Dunnhumby The Complete Journey Dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
import logging

from src.config.settings import dataset_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_raw_transactions(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load transactions with optimized memory downcasting.
    Reduces RAM footprint from ~350MB to ~70MB.
    """
    path = file_path or dataset_config.transaction_file
    logger.info(f"Loading transactions from {path}...")
    
    dtypes = {
        "household_key": "uint16",
        "BASKET_ID": "uint64",
        "DAY": "uint16",
        "PRODUCT_ID": "uint32",
        "QUANTITY": "int32",
        "SALES_VALUE": "float32",
        "STORE_ID": "uint16",
        "RETAIL_DISC": "float32",
        "TRANS_TIME": "uint16",
        "WEEK_NO": "uint8",
        "COUPON_DISC": "float32",
        "COUPON_MATCH_DISC": "float32",
    }
    
    df = pd.read_csv(path, dtype=dtypes)
    logger.info(f"Loaded {len(df):,} transactions across {df['household_key'].nunique():,} households.")
    return df


def load_products(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Load product catalog metadata."""
    path = file_path or dataset_config.product_file
    dtypes = {
        "PRODUCT_ID": "uint32",
        "MANUFACTURER": "category",
        "DEPARTMENT": "category",
        "BRAND": "category",
        "COMMODITY_DESC": "category",
        "SUB_COMMODITY_DESC": "category",
    }
    df = pd.read_csv(path, dtype=dtypes)
    logger.info(f"Loaded {len(df):,} products across {df['DEPARTMENT'].nunique():,} departments.")
    return df


def load_demographics(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load household demographics (801 households available).
    Maps ordinal classifications into readable categories.
    """
    path = file_path or dataset_config.demographic_file
    df = pd.read_csv(path)
    df["household_key"] = df["household_key"].astype("uint16")
    logger.info(f"Loaded demographics for {len(df):,} households ({len(df)/2500*100:.1f}% coverage).")
    return df


def load_campaigns() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load campaign descriptions and household-campaign assignments."""
    df_desc = pd.read_csv(dataset_config.campaign_desc_file)
    df_table = pd.read_csv(dataset_config.campaign_table_file)
    df_table["household_key"] = df_table["household_key"].astype("uint16")
    logger.info(f"Loaded {len(df_desc)} campaigns assigned to {df_table['household_key'].nunique()} households.")
    return df_desc, df_table


def load_coupons() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load coupon mappings and historical coupon redemptions."""
    df_coupon = pd.read_csv(dataset_config.coupon_file)
    initial_coupons = len(df_coupon)
    df_coupon = df_coupon.drop_duplicates()
    dups_removed = initial_coupons - len(df_coupon)

    df_redempt = pd.read_csv(dataset_config.coupon_redempt_file)
    df_redempt["household_key"] = df_redempt["household_key"].astype("uint16")
    df_redempt["DAY"] = df_redempt["DAY"].astype("uint16")
    logger.info(f"Loaded {len(df_coupon):,} unique coupon-product mappings (cleaned {dups_removed:,} exact duplicates) and {len(df_redempt):,} redemption events.")
    return df_coupon, df_redempt


def build_basket_dataset(df_trans: pd.DataFrame, df_prod: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Aggregate line-level transaction receipt rows into trip-level Baskets.
    Cleans out negative/void transactions and computes basket anatomy metrics.
    """
    logger.info("Aggregating transactions into trip-level Baskets...")
    
    # Identify perishable products if product catalog is supplied
    perish_ids = set()
    if df_prod is not None:
        perish_depts = dataset_config.perishable_departments
        perish_ids = set(df_prod[df_prod["DEPARTMENT"].isin(perish_depts)]["PRODUCT_ID"])
    
    # Flag perishable line items
    df_trans["is_perishable"] = df_trans["PRODUCT_ID"].isin(perish_ids) if perish_ids else False
    
    # Trip-level aggregation
    baskets = df_trans.groupby(["household_key", "BASKET_ID", "DAY", "STORE_ID"]).agg(
        basket_spend=("SALES_VALUE", "sum"),
        basket_items=("QUANTITY", "sum"),
        distinct_items=("PRODUCT_ID", "nunique"),
        retail_discount=("RETAIL_DISC", "sum"),
        coupon_discount=("COUPON_DISC", "sum"),
        has_perishable=("is_perishable", "any"),
        trans_time=("TRANS_TIME", "first"),
        week_no=("WEEK_NO", "first"),
    ).reset_index()
    
    # Clean non-positive spend trips (refunds/voids)
    initial_count = len(baskets)
    baskets = baskets[baskets["basket_spend"] > 0].copy()
    baskets.sort_values(["household_key", "DAY"], inplace=True)
    
    logger.info(f"Cleaned {initial_count - len(baskets):,} non-positive trips. Remaining valid baskets: {len(baskets):,}.")
    
    # Calculate inter-trip interval (days since previous trip for the same household)
    baskets["prev_day"] = baskets.groupby("household_key")["DAY"].shift(1)
    baskets["inter_trip_days"] = baskets["DAY"] - baskets["prev_day"]
    
    return baskets


class DataLoader:
    """Convenience wrapper for unified dataset ingestion and preparation."""

    @classmethod
    def load_all(cls) -> Dict[str, Any]:
        """Loads all relational tables with optimized data types."""
        trans = load_raw_transactions()
        prods = load_products()
        demos = load_demographics()
        camp_desc, camp_table = load_campaigns()
        coupon, coupon_redempt = load_coupons()
        return {
            "transactions": trans,
            "products": prods,
            "demographics": demos,
            "campaign_desc": camp_desc,
            "campaigns": camp_table,
            "coupons": coupon,
            "redemptions": coupon_redempt,
        }

    @classmethod
    def build_trip_level_baskets(cls, trans_df: pd.DataFrame, product_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Aggregates raw item transactions into trip-level basket summaries."""
        return build_basket_dataset(trans_df, product_df)
