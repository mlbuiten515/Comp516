from lxml import etree
import numpy as np
import pandas as pd


tree = etree.parse(r'data_cleaning\taxonomy10.xml')
root = tree.getroot()

root = root.find("{http://pds.nasa.gov/pds4/pds/v1}File_Area_Observational")
root = root.find("{http://pds.nasa.gov/pds4/pds/v1}Table_Character")
root = root.find("{http://pds.nasa.gov/pds4/pds/v1}Record_Character")

column_names = []
for column in root.findall("{http://pds.nasa.gov/pds4/pds/v1}Field_Character"):
    label = column.find("{http://pds.nasa.gov/pds4/pds/v1}name").text
    column_names.append(label)


taxonomy = pd.read_csv(r'data_cleaning\taxonomy10.tab', header=None, names=column_names, sep=r'\s+')
taxonomy.rename(columns={'AST_NUMBER': 'ASTEROID_NUMBER', 'BUS_DEMEO_CLASS': 'CLASS'}, inplace=True)
taxonomy['ASTEROID_NUMBER'] = taxonomy['ASTEROID_NUMBER'].replace(0, np.nan)
taxonomy['CLASS'] = taxonomy['CLASS'].replace('-', np.nan)

null_count_ser = pd.isnull(taxonomy).sum()
print(null_count_ser)

taxonomy['ASTEROID_NUMBER'] = taxonomy['ASTEROID_NUMBER'].fillna(taxonomy['PROV_ID'])
taxonomy['CLASS'] = taxonomy['CLASS'].fillna(taxonomy['BUS_CLASS'])
taxonomy['CLASS'] = taxonomy['CLASS'].fillna(taxonomy['THOLEN_CLASS'])

taxonomy = taxonomy[['ASTEROID_NUMBER', 'CLASS']]

taxonomy.to_csv('cleaned_taxonomy')
