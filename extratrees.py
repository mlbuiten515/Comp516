import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import sqlite3

family_data = r'data_cleaning\nesvorny_families.csv'
column_types = {'ASTEROID_NUMBER': int, 'A_PROP': float, 'PROPER_ECC': float,
                'SINE_PROPER_INCL': float, 'ABS_MAG': float, 'C_PARAM': float,
                'number': int, 'FAMILY_NUMBER': 'string', 'FAMILY_NAME': 'string'}

df = pd.read_csv(family_data, dtype=column_types)
headers = list(df.columns.values)

df['FAMILY_NUMBER'].replace('San', '626').apply(pd.to_numeric, errors='coerce')

y = df.iloc[:, -1]
X = df.iloc[:, 1:4]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = ExtraTreesClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


#num_score = accuracy_score(y_test['FAMILY_NUMBER'], y_pred[:, 0])
#name_score = accuracy_score(y_test['FAMILY_NAME'], y_pred[:, 1])

family_column_types = {'ASTEROID_NUMBER': int, 'PROVISIONAL_ID': 'string', 'PROPER_A': float, 'PROPER_ECC': float,
                    'SINE_PROPER_INCL': float, 'FAMILY_NAME': 'string', 'CLUMP_FLAG': 'string', 'CONFIDENCE_LEVEL': int}

family_df = pd.read_csv(r'data_cleaning\family_data.csv', dtype=family_column_types)

family_df.rename(columns={'PROPER_A': 'A_PROP'}, inplace=True)

family_df = family_df[family_df.FAMILY_NAME != '---']
family_df = family_df[family_df.PROVISIONAL_ID != '---']

X_over = family_df.iloc[:, 2:5]
y_over = family_df.iloc[:, -3]

family_pred = model.predict(X_over)

print(accuracy_score(y_over, family_pred))

#print(num_score, name_score)
