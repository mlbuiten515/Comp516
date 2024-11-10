import pandas as pd


nes_column_types = {'ASTEROID_NUMBER': int, 'A_PROP': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'ABS_MAG': float, 'C_PARAM': float,
                    'number': int, 'FAMILY_NUMBER': 'string', 'FAMILY_NAME': 'string'}

nesvorny_df = pd.read_csv(r'data_cleaning\nesvorny_families.csv', dtype=nes_column_types)

nesvorny_df['FAMILY_NUMBER'].replace('San', '626').apply(pd.to_numeric, errors='coerce')

family_column_types = {'ASTEROID_NUMBER': int, 'PROVISIONAL_ID': 'string', 'PROPER_A': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'FAMILY_NAME': 'string', 'CLUMP_FLAG': 'string', 'CONFIDENCE_LEVEL': int}

family_df = pd.read_csv(r'data_cleaning\family_data.csv', dtype=family_column_types)

family_df.rename(columns={'PROPER_A': 'A_PROP'}, inplace=True)

family_df = family_df[family_df.FAMILY_NAME != '---']
family_df = family_df[family_df.PROVISIONAL_ID != '---']

print(family_df.size)
