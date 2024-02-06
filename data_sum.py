import pandas as pd
import numpy as np

item_lines = pd.read_csv("7twenty_data/item_lines.csv")
# item_lines = pd.read_csv("Documents/BSC2/Master/Case Studies - Sia Partners/Code/7twenty_data/item_lines.csv")
item_lines.drop(columns=['Unnamed: 0', 'Cost'], inplace = True)

items = pd.read_csv("7twenty_data/items.csv")
# items = pd.read_csv("Documents/BSC2/Master/Case Studies - Sia Partners/Code/7twenty_data/items.csv")
items = items.rename(columns={"Item No": "Item"})
items.drop(columns=['Unnamed: 0', 'Item Name'], inplace = True)

# item_lines = item_lines.merge(items[["Item", "Hierarchy L2"]], on = "Item")
item_lines = item_lines.merge(items[["Item", "Hierarchy L3"]], on = "Item")
item_lines["Rev"] = item_lines['Amount'] * item_lines["Quantity"] #how to deal with returns? 

#item_lines = pd.get_dummies(item_lines, columns=['Hierarchy L2'], prefix='HL2', drop_first= True) * 1
item_lines = pd.get_dummies(item_lines, columns=['Hierarchy L3'], prefix='HL3', drop_first= True) * 1

#data = item_lines.groupby(["Receipt"], as_index=False).agg({'Rev': 'sum', **{f'HL2_{i}': 'first' for i in range(10, 25) if f'HL2_{i}' in item_lines.columns}})
data = item_lines.groupby(["Receipt"], as_index=False).agg({'Rev': 'sum', **{f'HL3_{i}': 'first' for i in range(100, 140) if f'HL3_{i}' in item_lines.columns}})

item_lines.drop_duplicates(subset = ["Receipt"], inplace = True)

item_lines["Y"] = np.where(item_lines["Customer ID"].isna(), 0, 1)
item_lines.drop(columns=['Customer ID'], inplace = True)

data = data.merge(item_lines[['Date', 'Time', 'Y', 'Receipt', 'Store']], on = 'Receipt')

del item_lines
del items

stores = pd.read_csv("7twenty_data/stores.csv")
# stores = pd.read_csv("Documents/BSC2/Master/Case Studies - Sia Partners/Code/7twenty_data/stores.csv")
stores = stores.rename(columns={"Store No_": "Store"})
stores.drop(columns=['Unnamed: 0', 'Store Name', "Last Date Modified"], inplace = True)

data = data.merge(stores, on = "Store")
data.drop(columns=["Store"], inplace = True)

del stores

data['Time'] = data['Time'].str[:2]
bins = [0, 6, 12, 18, 24]
labels = ['00:00-06:00', '06:00-12:00', '12:00-18:00', '18:00-00:00']
data['Time_interval'] = pd.cut(pd.to_numeric(data['Time']), bins=bins, labels=labels, right=False)
data = pd.get_dummies(data, columns=['Time_interval'], prefix='Hours', drop_first= True) * 1
#data = pd.get_dummies(data, columns=['Time'], prefix = 'Hour') * 1

days = [0, 1, 2, 3, 4]
weekend = [5, 6]

data['Day'] = pd.to_datetime(data['Date']).dt.dayofweek

data["Day"][data["Day"].isin(days)==True] = 0
data["Day"][data["Day"].isin(weekend)==True] = 1
data = pd.get_dummies(data, columns=['Day'], prefix='Weekend', drop_first= True) * 1

data = pd.get_dummies(data, columns=['Zone'], prefix='Zone', drop_first= True) * 1

data.drop(columns = ["Receipt", "Time"], inplace = True)

data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
split_date = pd.to_datetime('2023-04-4') #maybe another start date
subset_beforeT = data[data['Date'] < split_date].copy()
subset_afterT = data[data['Date'] >= split_date].copy()

del data

subset_afterT_member = subset_afterT[subset_afterT['Y'] == 1]

subset_afterT_nonmember = subset_afterT[subset_afterT['Y'] == 0]

del subset_afterT

subset_beforeT.to_csv('subset_beforeT.csv', index=False)
subset_afterT_member.to_csv('subset_afterT_member.csv', index=False)
subset_afterT_nonmember.to_csv('subset_afterT_nonmember.csv', index=False)





