import pandas as pd

file = '/home/kataha/New/IDH-Project/etl/data/SIPRI-Milex-data-1949-2023.xlsx'

sheet = pd.read_excel(file, 
    sheet_name = "Constant (2022) US$", 
    header= 5)
sheet = sheet.drop('Unnamed: 1', axis=1)
sheet = sheet.drop('Notes', axis = 1)
sheet.dropna(inplace=True)
sheet = pd.melt(sheet, id_vars=['Country'], value_vars=['1949'])
import pdb
pdb.set_trace()