from pathlib import Path
import pandas as pd


START_OF_VALIDATION_SET = "2019-03-01"
START_OF_TEST_SET = '2019-12-01'


all_tickers_folder = Path('data_feather/dukas_feather')

data_folder = all_tickers_folder.parent
for data_type in ['training', 'validation', 'test']:
	folder = data_folder / data_type
	folder.mkdir(exist_ok=True)


for ticker_file in all_tickers_folder.iterdir():
	df = pd.read_feather(ticker_file)

	training_set = df[df['datetime'] < START_OF_VALIDATION_SET]
	training_set.to_feather(data_folder / 'training' / ticker_file.name)

	validation_set = df[(df['datetime'] >= START_OF_VALIDATION_SET) & (df['datetime'] < START_OF_TEST_SET)]
	validation_set.reset_index(inplace=True)
	validation_set.to_feather(data_folder / 'validation' / ticker_file.name)

	test_set = df[df['datetime'] >= START_OF_TEST_SET]
	test_set.reset_index(inplace=True)
	test_set.to_feather(data_folder / 'test' / ticker_file.name)
	print(f"{ticker_file} done")


# test to make sure I didnt do mistakes
for ticker_file in (data_folder / 'training').iterdir():
	df = pd.read_feather(ticker_file)
	assert not (df['datetime'] >= START_OF_VALIDATION_SET).any()

for ticker_file in (data_folder / 'validation').iterdir():
	df = pd.read_feather(ticker_file)
	assert not ((df['datetime'] < START_OF_VALIDATION_SET) | (df['datetime'] >= START_OF_TEST_SET)).any()

for ticker_file in (data_folder / 'test').iterdir():
	df = pd.read_feather(ticker_file)
	assert not (df['datetime'] < START_OF_TEST_SET).any()

print("Done")

