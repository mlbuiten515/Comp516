from lxml import etree
import numpy as np
import pandas as pd

# Read in family column names from the .tab file
tree = etree.parse(r'data_cleaning\family.xml')
root = tree.getroot()


root = root.find("{http://pds.nasa.gov/pds4/pds/v1}File_Area_Observational")
root = root.find("{http://pds.nasa.gov/pds4/pds/v1}Table_Character")
root = root.find("{http://pds.nasa.gov/pds4/pds/v1}Record_Character")

family_column_names = {}
for column in root.findall("{http://pds.nasa.gov/pds4/pds/v1}Field_Character"):
    label = column.find("{http://pds.nasa.gov/pds4/pds/v1}name").text
    data_type = column.find("{http://pds.nasa.gov/pds4/pds/v1}data_type").text.split('_')[1]
    if data_type == 'Integer':
        family_column_names[label] = int
    elif data_type == 'String':
        family_column_names[label] = 'string'
    else:
        family_column_names[label] = float

# Import the family dataset and read into pandas

family_df = pd.read_csv(r'data_cleaning\family_data.csv',
                        dtype=family_column_names)

family_df.rename(columns={'PROPER_A': 'A_PROP'}, inplace=True)

# Remove data points with no identified family and simplify some family names

family_df = family_df[family_df.FAMILY_NAME != '---']
family_df['FAMILY_NAME'] = family_df['FAMILY_NAME'].replace('Polana(nysa)',
                                                            'Nysa-Polana')
family_df['FAMILY_NAME'] = family_df['FAMILY_NAME'].replace('Amneris(flora)',
                                                            'Flora')
family_df['FAMILY_NAME'] = family_df['FAMILY_NAME'].replace('Reginita(flora)',
                                                            'Flora')

family_df['ASTEROID_NUMBER'] = family_df['ASTEROID_NUMBER'].replace('-99999',
                                                                    np.nan)
family_df['ASTEROID_NUMBER'] = family_df['ASTEROID_NUMBER'].fillna(family_df['PROVISIONAL_ID'])

# Import the nesvorny dataset and read into pandas

nes_column_types = {'ASTEROID_NUMBER': 'string', 'A_PROP': float,
                    'PROPER_ECC': float, 'SINE_PROPER_INCL': float, 
                    'ABS_MAG': float, 'C_PARAM': float, 'number': int,
                    'FAMILY_NUMBER': 'string', 'FAMILY_NAME': 'string'}

nesvorny_df = pd.read_csv(r'data_cleaning\nesvorny_families.csv',
                          dtype=nes_column_types)

# In 2022 it was descovered that the san marcello family was actually the Kalliope family
nesvorny_df['FAMILY_NAME'].replace('Marcello', 'Kalliope')


# Drop columns to prepare to concatonate the two data frames

nesvorny_df = nesvorny_df.drop(columns=['ABS_MAG', 'C_PARAM',
                                        'number', 'FAMILY_NUMBER'])
family_df = family_df.drop(columns=['PROVISIONAL_ID', 'CLUMP_FLAG',
                                    'CONFIDENCE_LEVEL'])

# Create one table for family data and remove duplicate asteroids
asteroid_familys = pd.concat([family_df, nesvorny_df])
asteroid_familys = asteroid_familys.drop_duplicates(subset=['ASTEROID_NUMBER'],
                                                    keep='first')

asteroid_familys.to_csv('cleaned_families')
