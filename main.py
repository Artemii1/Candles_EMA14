import pandas as pd

#Function to aggregate price data to candles
def aggregate_to_candles(df, freq):
    try:
        # Resample the dataframe based on the timeframe
        ohlc = df['PRICE'].resample(freq).ohlc()

        return ohlc
    except Exception as e:
        print(f"Error in aggregate_to_candles: {e}")
        return None

#Function to calculate EMA
def compute_ema(prices, period):
    try:
        # Computing EMA using the pandas function
        ema = prices.ewm(span=period, adjust=False).mean()

        return ema
    except Exception as e:
        print(f"Error in compute_ema: {e}")
        return None

#Function to exclude empty rows from dataframe with aggregated candles
def remove_missing_rows(df_5min, df_1hour):
    """
    Removes rows from the given dataframes where the 'open' column has missing values.
    If 'open' value for row is empty, it means this candle doesn't have any price data. We can use any column to detect empty row.
    """
    # Remove rows from 5min dataframe where 'open' is NaN
    df_5min_cl = df_5min.dropna(subset=['open'])

    # Remove rows from 1hour dataframe where 'open' is NaN
    df_1hour_cl = df_1hour.dropna(subset=['open'])

    return df_5min_cl, df_1hour_cl

#This function isn't called at the moment and commented in main() function
def check_data(df_5min, df_1hour):

    while True:
        # Check if any rows have NaN values in 'open' column
        missing_data = df_5min[df_5min['open'].isna()]

        if missing_data.empty:
            break

        missing_data_start = missing_data.index[0]
        # Assuming continuous gaps, then the end of the gap is the next non-NaN data point
        missing_data_end = df_5min.loc[missing_data_start:].dropna().index[0] if len(df_5min.loc[missing_data_start:].dropna()) > 0 else None

        #Report the missing data period in console
        print(f"Data is missing from {missing_data_start.strftime('%H:%M %Y.%m.%d')} to {missing_data_end.strftime('%H:%M %Y.%m.%d') if missing_data_end else 'the end'}.")
        # Ask user whether to exclude data from the broken period till the end
        choice = input("Exclude data from broken period till the end, [Y/N]: ")
        if choice.lower() == 'y':
            # Remove data from the missing point till the end in 5min dataframe
            df_5min = df_5min[df_5min.index < missing_data_start]

            # If data breaks within an hour, remove the entire hour and data from the missing point till the end in 1hour dataframe
            if missing_data_start.minute != 0:
                hour_start = missing_data_start.replace(minute=0, second=0)
                df_1hour = df_1hour[df_1hour.index < hour_start]
            else:
                df_1hour = df_1hour[df_1hour.index < missing_data_start]
            break
        elif choice.lower() == 'n':
            # Fill missing rows with the last closing price from the previous candle
            last_valid_close = df_5min['close'].loc[:missing_data_start].last_valid_index()
            fill_value = df_5min.at[last_valid_close, 'close']
            df_5min.loc[missing_data_start:missing_data_end, ['open', 'close', 'high', 'low']] = fill_value

        else:
            print("Incorrect input")
            #Restart the function if input is incorrect
            test_data(df_5min, df_1hour)
            break
            
    #The functions returns upgraded dataframes if some issues found, or existing dataframes if not
    return df_5min, df_1hour



def main():
    try:
        # Reading the CSV file
        df = pd.read_csv("prices.csv", parse_dates=['TS'], index_col='TS')

        # Aggregating trades to candles
        df_5min = aggregate_to_candles(df, '5T')
        df_1hour = aggregate_to_candles(df, 'H')

        '''#The function below is commented due to a lot of missing data. Can be used for better data frames.

        #Function to check 5min data frame to exclude all the data from place,
        #where broken data is defined or fill the missing data with latest closing price, depending on users choice.
        df_5min, df_1hour = check_data(df_5min, df_1hour)'''

        #Removing missing rows, if there are some
        df_5min, df_1hour = remove_missing_rows(df_5min, df_1hour)

        # Computing the EMA for both timeframes, by taking close prices from dataframes to compute EMA, and adding the results of calculations in dataframes
        df_5min['EMA'] = compute_ema(df_5min['close'], 14)
        df_1hour['EMA'] = compute_ema(df_1hour['close'], 14)




        # Saving the results to CSV files
        df_5min.to_csv("5min_output.csv", columns=["open", "close", "high", "low", "EMA"])
        df_1hour.to_csv("1hour_output.csv", columns=["open", "close", "high", "low", "EMA"])

        print("Completed successfully!")
        return df_5min, df_1hour

    except Exception as e:
        print(f"Error in main function: {e}")
        return None, None

if __name__ == "__main__":
    main()
