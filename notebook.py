# %%
import pandas as pd
import requests
import json
df1 = pd.read_csv('vendor1.csv')
df1 = df1.drop(columns=['ID'])
df1 = df1.rename(columns={'vendor1_id': 'id', 'addr': 'street', 'zip': 'zip_code', 'phone_num': 'phone_number', 'dob': 'date_of_birth', 'date_registrated': 'registration_date'})
df1.head()
# %%
with open('vendor2.json') as f:
	results_list = []
	for line in f:
		obj = json.loads(line)
		results_list.append(obj)
# %%
df2 = pd.read_json(json.dumps(results_list))
df2 = df2.rename(columns={'vendor2_id': 'id', 'firstName': 'first_name', 'middleName': 'middle_name', 'lastName': 'last_name', 'addressLine1': 'street', 'zipCode': 'zip_code', 'phoneNum': 'phone_number', 'birthDate': 'date_of_birth', 'registrationDate': 'registration_date'})
df2.head()
# %%
r = requests.get('https://randomuser.me/api/?results=500&seed=0')
x = r.json()
df3 = pd.DataFrame(x['results'])
df3.head()
# %%
df3 = pd.json_normalize(json.loads(df3.to_json(orient='records')))
df3.head()
# %%
df3.columns
# %%
df3 = df3.rename(columns={'login.uuid': 'id', 'name.title': 'prefix', 
'name.first': 'first_name', 'name.last': 'last_name', 
'location.street': 'street', 'location.city': 'city', 
'location.state': 'state', 'location.postcode': 'zip_code', 
'dob.date': 'date_of_birth', 'registered.date': 'registration_date'})
df3.head()
# %%
with open('vendor2.json') as f:
	data = json.load(f)
data
# %%
