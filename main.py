import numpy as np
import pandas as pd


def split_scores(scores_string):
    scores = np.array([d.replace(',', '.') for d in scores_string.split('\n')[1].split('|')], dtype=float)
    return scores


def wrrc_score(scores_string):
    return float(scores_string.split('\n')[0].strip().replace(',', '.'))


def mean_score(scores_string):
    scores = split_scores(scores_string)
    return scores.mean()


def std_score(scores_string):
    scores = split_scores(scores_string)
    return scores.std()


def sum_score(scores_string):
    scores = split_scores(scores_string)
    return scores.sum()


def mean_score_maxmin(scores_string):
    scores = split_scores(scores_string)
    scores = np.delete(scores, scores.argmin())
    scores = np.delete(scores, scores.argmax())
    return scores.mean()


is_slow_fast = False
data_raw = pd.read_csv('stuttgart2022_semifinal.csv', sep=',', skiprows=2)

data_raw = data_raw.iloc[:-5]
if is_slow_fast:
    slow_data = data_raw.iloc[::2].reset_index(drop=True)
    rename_dict = dict()
    for old_col, new_col in zip(data_raw.columns[:-3], data_raw.columns[3:]):
        rename_dict[old_col] = new_col
    fast_data = data_raw.iloc[1::2].dropna(axis=1).rename(columns=rename_dict).reset_index(drop=True)
    fast_data[slow_data.columns[:3]] = slow_data[slow_data.columns[:3]]

    data = pd.concat([slow_data, fast_data])
else:
    data = data_raw.copy()

categories = ['BBW', 'BBM', 'LF', 'DF', 'MI']
categories_points = [7.5, 7.5, 15, 10, 25]

# notes = np.array([d.replace(',', '.') for d in data['BBW'].iloc[0].split('\n')[1].split('|')], dtype=float)
for category in categories:
    data[category + '_wrrc'] = data[category].map(wrrc_score)
    data[category + '_mean'] = data[category].map(mean_score)
    data[category + '_std'] = data[category].map(std_score)
    data[category + '_mean_maxmin'] = data[category].map(mean_score_maxmin)
    data[category + '_sum'] = data[category].map(sum_score)

# max_points = 65
judges = 8
# max_points_sum = judges * max_points

data['sum_cat'] = data[[cat + '_wrrc' for cat in categories]].sum(axis=1)
data['sum_all'] = data[[cat + '_sum' for cat in categories]].sum(axis=1)
data['mean_all'] = data['sum_all'] / judges
