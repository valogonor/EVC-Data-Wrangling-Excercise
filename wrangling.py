import json
import os
import pandas as pd
import requests

def json_to_df(filename):
	"""
	Reads a json file into a pandas dataframe
	:param filename: the path to the json file
	:return: the pandas dataframe
	"""
	with open(filename) as f:
		data = None
		try:
			data = json.load(f)
		except ValueError:
			try:
				with open(filename) as f:
					results_list = []
					for line in f:
						obj = json.loads(line)
						results_list.append(obj)
					df = pd.read_json(json.dumps(results_list))
					return df
			except ValueError:
				print('File is not valid JSON.')
		if data and type(data) is list:
			df = pd.read_json(json.dumps(data))
		elif data and type(data) is dict:
			# Assuming the first key is the valid key
			for key in data:
				df = pd.DataFrame(data[key])
				break
		df = pd.json_normalize(json.loads(df.to_json(orient='records')))
	return df

def clean_columns(df):
	"""
	This function takes in a dataframe, drops unnecessary columns,
	and standardizes the names of the columns.
	"""
	col_names = {}
	for col in df.columns:
		if 'id' == col[-2:]:
			col_names[col] = 'id'
		elif 'addr' in col:
			col_names[col] = 'street'
		elif 'zip' in col:
			col_names[col] = 'zip_code'
		elif 'phone' in col:
			col_names[col] = 'phone_number'
		elif 'dob' in col and 'age' not in col:
			col_names[col] = 'date_of_birth'
		elif 'birth' in col:
			col_names[col] = 'date_of_birth'
		elif 'regis' in col and ('registered' not in col or 'date' in col):
			col_names[col] = 'registration_date'
		elif 'title' in col:
			col_names[col] = 'prefix'
		elif 'first' in col:
			col_names[col] = 'first_name'
		elif 'last' in col:
			col_names[col] = 'last_name'
		elif 'middle' in col:
			col_names[col] = 'middle_name'
		elif 'code' in col:
			col_names[col] = 'zip_code'
		elif 'email' in col:
			col_names[col] = 'email'
		elif 'prefix' in col:
			col_names[col] = 'prefix'
		elif 'suffix' in col:
			col_names[col] = 'suffix'
		elif 'street' in col and 'number' not in col and 'name' not in col:
			col_names[col] = 'street'
		elif 'street' in col and 'number' in col:
			col_names[col] = 'street_number'
		elif 'street' in col and 'name' in col:
			col_names[col] = 'street_name'
		elif 'city' in col:
			col_names[col] = 'city'
		elif 'state' in col:
			col_names[col] = 'state'
	todrop = []
	for col in df.columns:
		if col not in col_names:
			todrop.append(col)
	df = df.drop(columns=todrop)
	df = df.rename(columns=col_names)
	if 'street_number' and 'street_name' in df.columns:
		df['street'] = df['street_number'].map(str) + ' ' + df['street_name']
		df = df.drop(columns=['street_number', 'street_name'])
	return df



# Enter any urls with data to be wrangled in urls list
urls = ['https://randomuser.me/api/?results=500&seed=0']
dataframes = []
# CSVs and JSONs are added to dataframes list
for file in os.listdir():
	if file.endswith('.csv'):
		df = pd.read_csv(file)
		dataframes.append(df)
	elif file.endswith('.json'):
		df = json_to_df(file)
		dataframes.append(df)
# Assumes that the urls are all JSONs
for url in urls:
	r = requests.get(url)
	x = r.json()
	if type(x) is list:
		df = pd.read_json(json.dumps(x))
	elif type(x) is dict:
		for key in x:
			df = pd.DataFrame(x[key])
			df = pd.json_normalize(json.loads(df.to_json(orient='records')))
			break
	dataframes.append(df)
for i, df in enumerate(dataframes):
	df = clean_columns(df)
	dataframes[i] = df
while len(dataframes) > 1:
	df2 = dataframes.pop()
	df1 = dataframes.pop()
	df = pd.concat([df1, df2], sort=False)
	dataframes.append(df)
df = dataframes[0]
df.to_csv('all_users.csv')