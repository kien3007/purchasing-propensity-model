"""
Multi-Dimensional Point-in-Time Feature Engineering Module
Guarantees absolute absence of data leakage (strictly DAY <= t_0).
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

from src.config.settings import time_config

logger = logging.getLogger(__name__)


class PointInTimeFeatureExtractor:
    """
    Extracts behavioral, monetary, cycle, marketing, store loyalty,
    and demographic features for each household as of an arbitrary cutoff date t_0.
    """
    def __init__(
        self,
        baskets_df: pd.DataFrame,
        campaigns_df: Optional[pd.DataFrame] = None,
        redemptions_df: Optional[pd.DataFrame] = None,
        demographics_df: Optional[pd.DataFrame] = None,
        lookback_days: int = time_config.observation_window_days,
    ):
        self.baskets = baskets_df
        self.campaigns = campaigns_df
        self.redemptions = redemptions_df
        self.demographics = demographics_df
        self.lookback_days = lookback_days
        self.all_households = pd.DataFrame({"household_key": list(range(1, 2501))})

    def extract_features_for_cutoff(self, t0: int) -> pd.DataFrame:
        """Extract all features for a single cutoff date t_0."""
        # 1. Slice strictly historical data (DAY <= t0 and DAY >= t0 - lookback_days)
        hist = self.baskets[(self.baskets["DAY"] <= t0) & (self.baskets["DAY"] >= t0 - self.lookback_days)].copy()
        
        # Base dataframe with all 2,500 households
        feats = self.all_households.copy()
        feats["cutoff_day"] = t0

        # --- A. Recency & Timing Dynamics ---
        # Latest trip date up to t0
        latest_trip = hist.groupby("household_key")["DAY"].max().reset_index()
        latest_trip.rename(columns={"DAY": "last_trip_day"}, inplace=True)
        feats = feats.merge(latest_trip, on="household_key", how="left")
        feats["days_since_last_basket"] = (t0 - feats["last_trip_day"]).fillna(self.lookback_days + 1)

        # Latest perishable purchase
        perish_hist = hist[hist["has_perishable"] == True]
        if not perish_hist.empty:
            latest_perish = perish_hist.groupby("household_key")["DAY"].max().reset_index()
            latest_perish.rename(columns={"DAY": "last_perish_day"}, inplace=True)
            feats = feats.merge(latest_perish, on="household_key", how="left")
            feats["days_since_last_perishable"] = (t0 - feats["last_perish_day"]).fillna(self.lookback_days + 1)
        else:
            feats["days_since_last_perishable"] = self.lookback_days + 1

        # Inter-trip cycle statistics
        inter_stats = hist.groupby("household_key")["inter_trip_days"].agg(["median", "std"]).reset_index()
        inter_stats.columns = ["household_key", "median_inter_trip", "std_inter_trip"]
        feats = feats.merge(inter_stats, on="household_key", how="left")
        feats["median_inter_trip"] = feats["median_inter_trip"].fillna(self.lookback_days)
        feats["std_inter_trip"] = feats["std_inter_trip"].fillna(0)

        # Critical Feature: Urgency Ratio (Personalized Lateness)
        feats["urgency_ratio"] = feats["days_since_last_basket"] / (feats["median_inter_trip"] + 1e-5)

        # --- B. Frequency & Momentum ---
        for window in [14, 30, 60, 90, 180]:
            sub = hist[hist["DAY"] >= t0 - window]
            counts = sub.groupby("household_key")["BASKET_ID"].nunique().reset_index()
            counts.columns = ["household_key", f"baskets_count_{window}d"]
            feats = feats.merge(counts, on="household_key", how="left")
            feats[f"baskets_count_{window}d"] = feats[f"baskets_count_{window}d"].fillna(0)

        # Frequency Momentum (Short-term velocity vs Baseline)
        feats["frequency_momentum_30_vs_90"] = (
            (feats["baskets_count_30d"] / 30.0) / 
            ((feats["baskets_count_90d"] / 90.0) + 1e-5)
        )

        # --- C. Monetary & Basket Architecture ---
        for window in [30, 90, 180]:
            sub = hist[hist["DAY"] >= t0 - window]
            spend = sub.groupby("household_key")["basket_spend"].sum().reset_index()
            spend.columns = ["household_key", f"spend_{window}d"]
            feats = feats.merge(spend, on="household_key", how="left")
            feats[f"spend_{window}d"] = feats[f"spend_{window}d"].fillna(0)

        feats["aov_90d"] = feats["spend_90d"] / (feats["baskets_count_90d"] + 1e-5)

        # Average items and department breadth in 90 days
        sub90 = hist[hist["DAY"] >= t0 - 90]
        if not sub90.empty:
            avg_items = sub90.groupby("household_key")["basket_items"].mean().reset_index()
            avg_items.columns = ["household_key", "avg_items_per_basket_90d"]
            feats = feats.merge(avg_items, on="household_key", how="left")
            feats["avg_items_per_basket_90d"] = feats["avg_items_per_basket_90d"].fillna(0)

            # Perishable basket proportion
            perish_ratio = sub90.groupby("household_key")["has_perishable"].mean().reset_index()
            perish_ratio.columns = ["household_key", "perishable_basket_ratio_90d"]
            feats = feats.merge(perish_ratio, on="household_key", how="left")
            feats["perishable_basket_ratio_90d"] = feats["perishable_basket_ratio_90d"].fillna(0)
        else:
            feats["avg_items_per_basket_90d"] = 0
            feats["perishable_basket_ratio_90d"] = 0

        # --- D. Marketing & Coupon Responsiveness ---
        if self.campaigns is not None and not self.campaigns.empty:
            # Active campaigns at t0
            active_camps = self.campaigns[
                (self.campaigns["START_DAY"] <= t0) & (self.campaigns["END_DAY"] >= t0)
            ]
            active_hh = set(active_camps["household_key"].unique())
            feats["is_targeted_by_active_campaign"] = feats["household_key"].isin(active_hh).astype(int)
        else:
            feats["is_targeted_by_active_campaign"] = 0

        if self.redemptions is not None and not self.redemptions.empty:
            # Historical coupon redemptions up to t0
            hist_red = self.redemptions[
                (self.redemptions["DAY"] <= t0) & (self.redemptions["DAY"] >= t0 - self.lookback_days)
            ]
            red_counts = hist_red.groupby("household_key")["COUPON_UPC"].count().reset_index()
            red_counts.columns = ["household_key", "coupon_redemption_count_180d"]
            feats = feats.merge(red_counts, on="household_key", how="left")
            feats["coupon_redemption_count_180d"] = feats["coupon_redemption_count_180d"].fillna(0)
        else:
            feats["coupon_redemption_count_180d"] = 0

        # --- E. Store Loyalty ---
        if not hist.empty:
            store_agg = hist.groupby(["household_key", "STORE_ID"])["basket_spend"].sum().reset_index()
            primary_store = store_agg.sort_values(["household_key", "basket_spend"], ascending=[True, False]).groupby("household_key").first().reset_index()
            primary_store.rename(columns={"STORE_ID": "primary_store_id", "basket_spend": "primary_store_spend"}, inplace=True)
            
            feats = feats.merge(primary_store[["household_key", "primary_store_id", "primary_store_spend"]], on="household_key", how="left")
            feats["store_loyalty_index"] = (feats["primary_store_spend"] / (feats["spend_180d"] + 1e-5)).fillna(0).clip(0, 1)
            feats["primary_store_id"] = feats["primary_store_id"].fillna(0).astype("category")
        else:
            feats["primary_store_id"] = 0
            feats["store_loyalty_index"] = 0

        # --- F. Demographics ---
        if self.demographics is not None:
            demo_cols = [
                "household_key", "classification_1", "classification_2", "classification_3",
                "HOMEOWNER_DESC", "classification_4", "classification_5", "KID_CATEGORY_DESC"
            ]
            avail_cols = [c for c in demo_cols if c in self.demographics.columns]
            feats = feats.merge(self.demographics[avail_cols], on="household_key", how="left")
            # Fill missing with UNKNOWN
            for c in avail_cols:
                if c != "household_key":
                    feats[c] = feats[c].fillna("UNKNOWN").astype("category")

        # Cleanup intermediate helper columns
        drop_cols = ["last_trip_day", "last_perish_day", "primary_store_spend"]
        feats.drop(columns=[c for c in drop_cols if c in feats.columns], inplace=True)

        return feats

    def extract_multi_cutoff_features(self, cutoffs: List[int]) -> pd.DataFrame:
        """Extract and concatenate features across multiple cutoff dates."""
        dfs = []
        for t0 in cutoffs:
            logger.info(f"Extracting Point-in-Time features for cutoff t_0={t0}...")
            dfs.append(self.extract_features_for_cutoff(t0))
        return pd.concat(dfs, ignore_index=True)
