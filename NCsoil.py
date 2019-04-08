import argparse

import pandas

excl_path = './NCSOIL_input'
csv_path  = './NCSOILI'

excl_data = pandas.read_excel(excl_path,header=None)
input_data = excl_data.T
input_data.to_csv(csv_path)



