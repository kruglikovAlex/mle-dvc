import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
import yaml
import os
import json
import joblib

def evaluate_model():
    
    # Прочитаем файл с гиперпараметрами params.yaml
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd) 

    # загружаем результат шага 1: inital_data.csv
    data = pd.read_csv('data/initial_data.csv')

    # загружаем результат шага 2: загрузка модели
    with open('models/fitted_model.pkl', 'rb') as fd:
        pipeline = joblib.load(fd)

    # Проверка качества на кросс-валидации
    cv_strategy = StratifiedKFold(n_splits=params['n_splits'])
    cv_res = cross_validate(
        pipeline,
        data,
        data[params['target_col']],
        cv=cv_strategy,
        n_jobs=params['n_jobs'],
        scoring=params['metrics']
    )

    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3) 

    # сохраните результата кросс-валидации в cv_res.json
    os.makedirs('cv_results', exist_ok=True) # создание директории, если её ещё нет
    with open('cv_results/cv_res.json', 'w') as fd: # запись в файл
        fd.write(json.dumps(cv_res))


if __name__ == '__main__':
	evaluate_model()