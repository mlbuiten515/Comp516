import pandas as pd
import numpy as np

# Import the nesvorny dataset and read into pandas

nes_column_types = {'ASTEROID_NUMBER': 'string', 'A_PROP': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'ABS_MAG': float, 'C_PARAM': float,
                    'number': int, 'FAMILY_NUMBER': 'string', 'FAMILY_NAME': 'string'}

nesvorny_df = pd.read_csv(r'data_cleaning\nesvorny_families.csv', dtype=nes_column_types)

# In 2022 it was descovered that the san marcello family was actually the Kalliope family
nesvorny_df['FAMILY_NAME'].replace('Marcello', 'Kalliope')

# Import the family dataset and read into pandas

family_column_types = {'ASTEROID_NUMBER': 'string', 'PROVISIONAL_ID': 'string', 'PROPER_A': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'FAMILY_NAME': 'string', 'CLUMP_FLAG': 'string', 'CONFIDENCE_LEVEL': int}

family_df = pd.read_csv(r'data_cleaning\family_data.csv', dtype=family_column_types)

family_df.rename(columns={'PROPER_A': 'A_PROP'}, inplace=True)

# Remove data points with no identified family and simplify some family names

family_df = family_df[family_df.FAMILY_NAME != '---']
family_df['FAMILY_NAME'].replace('Polana(nysa)', 'Nysa-Polana', inplace=True)
family_df['FAMILY_NAME'].replace('Amneris(flora)', 'Flora', inplace=True)
family_df['FAMILY_NAME'].replace('Reginita(flora)', 'Flora', inplace=True)

family_df['ASTEROID_NUMBER'].replace('-99999', np.nan, inplace=True)
family_df['ASTEROID_NUMBER'].fillna(family_df['PROVISIONAL_ID'], inplace=True)

# Drop columns to prepare to concatonate the two data frames

nesvorny_df = nesvorny_df.drop(columns=['ABS_MAG', 'C_PARAM', 'number', 'FAMILY_NUMBER'])
family_df = family_df.drop(columns=['PROVISIONAL_ID', 'CLUMP_FLAG', 'CONFIDENCE_LEVEL'])

# Create one table for family data and remove duplicate asteroids
asteroid_familys = pd.concat([family_df, nesvorny_df])
asteroid_familys = asteroid_familys.drop_duplicates(subset=['ASTEROID_NUMBER'], keep='first')



# Import spectral data and read into pandas 
main_belt_types = {'asteroid number': 'string', 'asteroid name': 'string',
                   'wavelength': float, 'reflectance': float,
                   'uncertainty': float}

main_belt_df = pd.read_csv(r'data_cleaning\Reddy_Main_Belt_Asteroid_Spectra\combined_spectral_data.csv', dtype=main_belt_types)

print(main_belt_df.head())