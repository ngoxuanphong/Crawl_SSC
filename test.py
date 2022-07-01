from base import getlink
import os
import pandas as pd
import multiprocessing

p = 'A:/DataLake/SSC/Phase2/'
ps_y = f'{p}Year/'
ps_q = f'{p}Quarter/'

list_folder=[p, ps_y, ps_q]
for folder in list_folder:
    if (os.path.exists(folder) == False) or (os.path.isdir(folder) == False):
        os.mkdir(folder)

all_com = pd.read_excel('base/data/AllCompanyDone.csv')['Symbol']
Symbol = list(all_com)[840:]

def KeoBaoCaoTaiChinhNam(symbol):
    print(Symbol, end = '___')
    web  = getlink.get()
    for year in ['2017', '2018', '2019', '2020', '2021']:
        web.login(symbol, year, 'NAM').to_csv(f'{ps_y}{symbol}_{year}.csv', index = False)
    for quy in range(1,5):
        for nam in range(2017, 2022):
            year = f'QUÝ {quy} {nam}'
            web.login(symbol, year, 'QUY').to_csv(f'{ps_q}{symbol}_{year}.csv', index = False)
    web.login(symbol, year, 'QUY').to_csv(f'{ps_q}{symbol}_QUÝ 1 2022.csv', index = False)
    print('Done')

def multip():
    pool = multiprocessing.Pool(processes=10)
    for symbol in Symbol:
      pool.apply_async(KeoBaoCaoTaiChinhNam,args=(symbol,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    multip()

# print(Symbol)