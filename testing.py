import unittest
import pandas as pd
from main import compute_ema, main
import numpy as np


class TestDataIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This will run once before any test in the class
        cls.df_5min, cls.df_1hour = main()

    def check_missing_values(self, df):
        for col in ["open", "close", "high", "low"]:
            if df[col].isna().any():
                missing_rows = np.where(df[col].isna())[0]
                raise AssertionError(f"Missing values found in {col} column at rows: {missing_rows}")


    def test_missing_values_5min(self):
        self.check_missing_values(self.df_5min)

    def test_missing_values_1hour(self):
        self.check_missing_values(self.df_1hour)

    def check_ema_calculation(self, df, period=14):
        computed_ema = compute_ema(df['close'], period) # Ensure compute_ema is available
        discrepancy = (computed_ema.iloc[period-1:] != df['EMA'].iloc[period-1:])
        if discrepancy.any():
            wrong_rows = np.where(discrepancy)[0] + period - 1 # Adjust for the offset introduced by iloc
            raise AssertionError(f"EMA not matching with the computed values from the 14th candle onwards at rows: {wrong_rows}")

    def test_ema_5min(self):
        self.check_ema_calculation(self.df_5min)

    def test_ema_1hour(self):
        self.check_ema_calculation(self.df_1hour)

if __name__ == "__main__":
    unittest.main()
