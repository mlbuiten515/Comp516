import glob
import pandas as pd

spectra_columns = ['WAVELENGTH', 'REFLECTANCE', 'ERROR']

# Read in spectral data from marsset2022 and combine

li = []

for filename in glob.glob(r'data_cleaning\marsset2022\*.csv'):
    x = filename.split('\\')
    asteroid_num = x[-1].split('_')[0]
    frame = pd.read_csv(filename, header=None, names=spectra_columns)
    fraame = frame.drop(columns='ERROR')
    frame = frame.pivot_table(index=None, columns='WAVELENGTH', values='REFLECTANCE', aggfunc='first')
    frame = frame.sort_index(axis=1)
    frame['ASTEROID_NUMBER'] = asteroid_num
    frame = frame.rename_axis(index=None, columns=None).reset_index(drop=True)
    li.append(frame)

marsset_data = pd.concat(li, ignore_index=True)

# define a function to check if the wavelength ends in 0 or 5 - based on our selected features.


def wavelength_check(val):
    if isinstance(val, float):
        if val < 0.45 or val > 2.45:
            return False 
        sig_digits = str(val)
    return sig_digits.endswith(('0', '5'))


filtered_columns = [col for col in marsset_data.columns if not isinstance(col, float) or wavelength_check(col)]
marsset_data = marsset_data[filtered_columns]

# Sort marsset_data columns numerically
numeric_cols = [col for col in marsset_data.columns if isinstance(col, (int, float))]
string_cols = [col for col in marsset_data.columns if isinstance(col, str)]

numeric_cols_sorted = sorted(numeric_cols)
string_cols_sorted = sorted(string_cols)

sorted_columns = numeric_cols_sorted + string_cols_sorted

marsset_data = marsset_data[sorted_columns]


