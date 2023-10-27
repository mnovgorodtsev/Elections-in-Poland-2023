import pandas as pd
import matplotlib.pyplot as plt
from geopandas import gpd

pd.set_option('display.max_columns', None)
def create_map(region_stats_dataset):
    PATH = r'C:\Users\AT-OUTLET\Desktop\powiatyPL\granice_powiatow\A02_Granice_powiatow.shp'
    poland_map = gpd.read_file(PATH, encoding='utf-8')

    poland_map = poland_map.rename(columns={"JPT_NAZWA_": "Powiat"})

    stats_dataset = pd.read_csv(region_stats_dataset+'.csv')

    # renaming part of districts to have same
    stats_dataset['Powiat'] = stats_dataset['Powiat'].str.replace('Miasto na prawach powiatu', 'Powiat')
    # creating new column with % rate
    stats_dataset['Rate'] = (stats_dataset['Laczna ilosc glosow niewaznych'] / stats_dataset[
        'Laczna ilosc glosow']) * 100

    merged_polish_map = poland_map.merge(stats_dataset, left_on=poland_map['Powiat'].str.lower(),
                                         right_on=stats_dataset['Powiat'].str.lower())

    cmap = 'coolwarm'
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    merged_polish_map.plot(column='Rate', cmap=cmap, legend=True, ax=ax)
    plt.title("Liczba głosów nieważnych (%)")
    plt.show()
