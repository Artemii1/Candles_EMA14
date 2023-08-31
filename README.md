# Creating a Candlestick Chart and Calculate the Exponential Moving Average (EMA)

This repository contains scripts to process trade data, aggregate them into candles, compute EMA (14), and test the integrity of the processed data.

## Overview

- `main.py`: Contains the primary functions to process and aggregate trade data into OHLC (Open-High-Low-Close) candles for two timeframes: 5 minutes and 1 hour. It also computes a 14-period Exponential Moving Average (EMA) for both timeframes.
- `testing.py`: A testing script to ensure the integrity of the data processed by `main.py`. It checks output data for missing values and validates the correctness of the computed EMA.
- `requirements.txt`: A list of Python packages that are required to run the scripts.

## Detailed description

`main.py` has 2 different functions to avoid gaps in output data, second function is manually disabled at the moment, but can be used in better data frames, than provided in `prices.csv`:


- `remove_missing_rows()`: this function simply remove empty rows from output dataframes

- `check_data()`: function is a bit more complicated (now disabled in code). This function analyses data (in 5-min candles dataframe) to find gaps. If gap is found function informs you in console, providing the gap interval. After that it's asking for user's choice: to fill the missing data with latest closing price (more suitable for small gaps) to minimize EMA dependence on gaps. The second choice is to delete all the data from the beginning of the gap till the end of dataframe. This option should be used, if we need strict results.

Please, note that both function doesn't help to avoid data mistakes inside 5 min candle. To do it script can be simply modified to create additional dataframe with smaller period, to improve output data results in other dataframes.


## Additional info

- Output samples of processing 'prices.csv' provided in this repo inside 'output' folder.
- All the notes and comments in script provided in English (as the task also in English), but I can simply translate them for you in Russian if needed.
