#!/bin/usr/env python3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if __name__ == '__main__':
    df = pd.read_csv('sector_data.csv',
                     index_col=0,
                     usecols=[1, 4],
                     names=['Sector' , 'Return'])
    df = df.groupby(['Sector']).mean()
    print(df)
    sns.barplot(x=df.index, y=df.Return)
    plt.xticks(rotation=45)
    plt.show()
