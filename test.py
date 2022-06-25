from base import getlink
import os
import pandas as pd

p = 'A:/DataLake/SSC/Phase1/'
ps_finan = f'{p}Financial/'
ps_y = f'{ps_finan}Year/'
ps_q = f'{ps_finan}Quarter/'

ps_y_BS = f'{ps_y}BalanceSheet/'
ps_y_IS = f'{ps_y}IncomeStatement/'
ps_y_CF = f'{ps_y}CashFlow/'

ps_q_BS = f'{ps_q}BalanceSheet/'
ps_q_IS = f'{ps_q}IncomeStatement/'
ps_q_CF = f'{ps_q}CashFlow/'

web  = getlink.get()
list_folder=[p, ps_finan, ps_y, ps_q, 
            ps_y_BS, ps_y_CF, ps_y_IS, 
            ps_q_BS, ps_q_CF, ps_q_IS,]

for folder in list_folder:
    if (os.path.exists(folder) == False) or (os.path.isdir(folder) == False):
        os.mkdir(folder)

symbol = 'AAA'
year = '2021'
all_com = pd.read_excel('base/data/List_Com_First (1_4).xlsx')['Symbol']
all_com = list(all_com)
for i in range(0, len(all_com)):
    symbol = all_com[i]
    print(i, symbol)
    for finan in ['BS']:
        for year in ['2018', '2019', '2020', '2021']:
            if finan == 'BS':
                web.login(symbol, year, finan).to_csv(f'{ps_y_BS}{year}{symbol}.csv', index = False)
            if finan == 'IS':
                web.login(symbol, year, finan).to_csv(f'{ps_y_IS}{year}{symbol}.csv', index = False)
