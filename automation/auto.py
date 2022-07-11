import schedule
import time
import logging

import financial_data as fd
import calls


# Getting list of companies currently tracked by SP500
curr_sp500 = fd.get_sp500_tickers()

# Getting list of companies currently tracked in DB
db_sp500 = calls.get_tickers()

# comparing the SP500 against the DB
missing = list()
excess = list()

if db_sp500 == None:
    missing = curr_sp500
else:
    # finding companies missing from DB
    for company in curr_sp500:
        if company not in db_sp500:
            missing.append(company)

    # finding companies no longer needed in DB
    for company in db_sp500:
        if company not in curr_sp500:
            excess.append(company)

# dropping excess tables
# need to handle response errors via logging
for ticker in excess:
    calls.drop_ticker(ticker)

# creating new tables and adding data
# need to handle errors with logging
# may be able to use df.to_sql to make this more efficient but this will bypass the API and require a seperate connection to the DB
for ticker in missing:
    calls.create_ticker(ticker)

    df = fd.get_full_hist(ticker)

    for idx, row in df.iterrows():
        calls.post_data(
            ticker=row["ticker"],
            date=row["date"],
            high=row["high"],
            low=row["low"],
            open=row["open"],
            close=row["close"],
            volume=row["volume"],
        )
