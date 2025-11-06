import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geodatasets
from collections import Counter
import nltk
from nltk.corpus import stopwords


def plot_individ_word_hist(benchmark_name, plot_name, word_list, output_dir, title_addition="", figsize=(4,4)):
    nltk.download('stopwords')
    stop = set(stopwords.words('english'))
    counter = Counter(word_list)
    most = counter.most_common()
    x, y = [], []
    for word, count in most[:100]:
        if (word not in stop):
            x.append(word)
            y.append(count)
    sns.set_theme(rc={"figure.figsize": figsize})
    sns.barplot(x=y, y=x)
    plt.title(f"Most frequent words - {benchmark_name}{title_addition}", fontsize=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{plot_name}.png'), format='png')


def plot_feature_barplot(benchmark_name, plot_name, data_list, output_dir, figsize=(3,3), topk=10, title_addition=""):
    sns.set_theme(rc={"figure.figsize": figsize})
    series = pd.Series(data_list)
    percentages = series.value_counts().values[:topk] / len(series) * 100
    indices = series.value_counts().index[:topk]
    print("Num. cases", len(series))
    print(dict(zip(indices, percentages)))
    sns.barplot(x=percentages, y=indices)
    plt.title(f"Top-{topk} {plot_name} - {benchmark_name}{title_addition}", fontsize=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{benchmark_name.lower()}_{plot_name}.png'), format='png')


def plot_map_distribution(benchmark_name, plot_name, coordinates_list, output_dir, title_addition=""):
    res = lambda x_l: [float(x) for x in x_l.replace("Point(", "").replace(")", "").split(' ')]

    geometry = [Point(res(x)) for x in coordinates_list if not x is None and x.startswith("Point")]
    gdf = GeoDataFrame(geometry, geometry=geometry)

    # this is a simple map that goes with geopandas
    world = gpd.read_file(geodatasets.data.naturalearth.land['url'])
    gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15)
    plt.title(benchmark_name + title_addition, fontsize=18)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{benchmark_name.lower()}_{plot_name}.png'), format='png')


def _format_time_to_years(times_list):
    times_formatted = []
    for date_str in times_list:
        if date_str.startswith("http"):
            continue
        if date_str[0] == '+':
            date_str = date_str[1:]
        # Remove missing month/day
        date_str = date_str.split('-00', maxsplit=1)[0]
        # Parse date
        dt = np.datetime64(date_str)
        times_formatted += [dt.astype('datetime64[Y]').astype(np.int64) + 1970]
    return times_formatted

def plot_times(benchmark_name, plot_name, times_list, output_dir, figsize=(5, 4)):
    print(times_list[:10])
    times_formatted = _format_time_to_years(times_list)
    time_frequencies = pd.Series(times_formatted).value_counts()
    time_df = pd.DataFrame()
    time_df["year"] = time_frequencies.index
    time_df["count"] = time_frequencies.values

    bins_manual = [0, 1000, 1500, 1600, 1700, 1800, 1900, 2000, 2025]
    time_df["time_bin"] = ["placeholder"] * len(time_df)
    time_df["bin_upper_bound"] = [1] * len(time_df)
    last_bin = -1
    for bin in bins_manual:
        for i, row in time_df.iterrows():
            if row["time_bin"] == "placeholder":
                if last_bin == -1:
                    if row["year"] <= bin:
                        time_df.loc[i, "time_bin"] = f"until {bin}"
                        time_df.loc[i, "bin_upper_bound"] = bin
                else:
                    if last_bin < row["year"] <= bin:
                        time_df.loc[i, "time_bin"] = f"until {bin}"
                        time_df.loc[i, "bin_upper_bound"] = bin
        last_bin = bin

    sns.set_theme(rc={"figure.figsize": figsize})  # width=3, #height=4
    time_df = time_df.sort_values("bin_upper_bound")
    time_df["time_bin"].hist()
    plt.xticks(rotation=45)
    plt.title("Time coverage", fontsize=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{benchmark_name.lower()}_{plot_name}.png'), format='png')