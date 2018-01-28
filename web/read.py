import pandas as pd 

data = pd.read_csv('static/data/learn/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv')

counties = data['BENE_COUNTY_CD'].values

print(list(set(counties)))


state_list = ['AK',
'AL',
'AR',
'AZ',
'CA',
'CO',
'CT',
'DE',
'FL',
'GA',
'HI',
'IA',
'ID',
'IL',
'IN',
'KS',
'KY',
'LA',
'MA',
'MD',
'ME',
'MI',
'MN',
'MO',
'MS',
'MT',
'NC',
'ND',
'NE',
'NH',
'NJ',
'NM',
'NV',
'NY',
'OH',
'OK',
'OR',
'PA',
'RI',
'SC',
'SD',
'TN',
'TX',
'UT',
'VA',
'VT',
'WA',
'WI',
'WV',
'WY']

state_dict = {}

start = 1
for state in state_list:
    state_dict[state.lower()] = start
    start+=1

start = 1
start_number_dict = {}
for state in state_list:
    start_number_dict[start] = state.lower()
    start+=1

print(start_number_dict)

print(state_dict)

# state_list=['AL','AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI','ID','IL','IN', 'IA','KS','KY','LA','ME','MD
# Massachusetts - MA
# Michigan - MI
# Minnesota - MN
# Mississippi - MS
# Missouri - MO
# Montana - MT
# Nebraska - NE
# Nevada - NV
# New Hampshire - NH
# New Jersey - NJ
# New Mexico - NM
# New York - NY
# North Carolina - NC
# North Dakota - ND
# Ohio - OH
# Oklahoma - OK
# Oregon - OR
# Pennsylvania - PA
# Rhode Island - RI
# South Carolina - SC
# South Dakota - SD
# Tennessee - TN
# Texas - TX
# Utah - UT
# Vermont - VT
# Virginia - VA
# Washington - WA
# West Virginia - WV
# Wisconsin - WI
# Wyoming - WY
# "