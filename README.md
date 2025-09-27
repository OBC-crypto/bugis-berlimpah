# bugis-berlimpah

Command Download Data

sudo docker compose run --rm freqtrade download-data --config user_data/config.json --timerange 20220101-20250922 --timeframe 3m 15m 1h


sudo docker compose run --rm freqtrade download-data --config user_data/config.json --days 30 -t 5m

#testing

sudo docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy FreqaiExampleHybridStrategy --freqaimodel LightGBMRegressor --timerange 20210101-20250922

sudo docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy FreqaiExampleHybridStrategy --freqaimodel CatboostRegressor --timerange 20210101-20250922

sudo docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy FreqaiExampleHybridStrategy --freqaimodel XGBoostRegressor --timerange 20210101-20250922

#dry-run

sudo docker compose run --rm freqtrade trade --config user_data/config.json --strategy SampleStrategy
