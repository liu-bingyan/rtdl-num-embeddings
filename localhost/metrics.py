import json
from pathlib import Path

import pandas as pd

def metrics(name = 'metrics'):
    df = pd.json_normalize([
        json.loads(x.read_text())
        for x in Path('exp').glob('mlp/*/0_evaluation/*/report.json')
    ])
    if name == 'metrics':
        print(df.groupby('config.data.path')['metrics.test.score'].mean().round(3))
    if name == 'hyperparameters':
        print(df[df['config.seed'] == 0]['config.training.lr'].quantile(0.5))

if __name__ == '__main__':
    namelist = ['metrics', 'hyperparameters']
    metrics('metrics')