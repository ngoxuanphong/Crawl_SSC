from base import getlink
import os
import pandas as pd

p = 'A:/DataLake/SSC/Phase1/'
ps_y = f'{p}Year/'
ps_q = f'{p}Quarter/'


web  = getlink.get()
list_folder=[p, ps_y, ps_q, ]

for folder in list_folder:
    if (os.path.exists(folder) == False) or (os.path.isdir(folder) == False):
        os.mkdir(folder)

symbol = '24H'
year = '2021'
all_com = pd.read_excel('base/data/List_Com_First (1_4).xlsx')['Symbol']
all_com = list(all_com)
for i in range(0, len(all_com)):
    symbol = all_com[i]
    print(i, symbol, end='__:')
    for finan in ['BS', 'IS']:
        for year in ['2018', '2019', '2020', '2021']:
            web.login(symbol, year, finan).to_csv(f'{ps_y}{symbol}_{year}_{finan}.csv', index = False)
    print('Done')

# finan = 'IS'