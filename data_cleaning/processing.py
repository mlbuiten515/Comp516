import pandas as pd


fam_column_types = {'ASTEROID_NUMBER': int, 'A_PROP': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'ABS_MAG': float, 'C_PARAM': float,
                    'number': int, 'FAMILY_NUMBER': 'string', 'FAMILY_NAME': 'string'}

family_df = pd.read_csv(r'data_cleaning\nesvorny_families.csv', dtype=fam_column_types)

family_df['FAMILY_NUMBER'].replace('San', '626').apply(pd.to_numeric, errors='coerce')

