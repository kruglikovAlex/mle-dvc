## scripts/data.py

# 1 — импорты
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml

# 2 — вспомогательные функции
def create_connection():

    load_dotenv()
    
    host = 'rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net' # os.environ.get('rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net')
    port = 6432 # os.environ.get('6432')
    db = 'playground_mle_20250507_60d03b0a2f' # os.environ.get('playground_mle_20250507_60d03b0a2f')
    username = 'mle_20250507_60d03b0a2f_freetrack' # os.environ.get('mle_20250507_60d03b0a2f_freetrack')
    password = 'c2538958c7974067a843c0a10811d6db' # os.environ.get('c2538958c7974067a843c0a10811d6db')
    
    print(f'postgresql://{username}:{password}@{host}:{port}/{db}')
    conn = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}', connect_args={'sslmode':'require'})
    return conn

# 3 — главная функция
def get_data():

    # 3.1 — загрузка гиперпараметров
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)

    # 3.2 — загрузки предыдущих результатов нет, так как это первый шаг

    # 3.3 — основная логика
    conn = create_connection()
    data = pd.read_sql('select * from clean_users_churn', conn, index_col=params['index_col'])
    conn.dispose()

    # 3.4 — сохранение результата шага
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/initial_data.csv', index=None)

# 4 — защищённый вызов главной функции
if __name__ == '__main__':
    get_data() 