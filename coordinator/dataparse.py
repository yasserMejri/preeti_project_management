import pandas as pd
import numpy as np
import seaborn as sns
from wlogger import Logger
import matplotlib.pyplot as plt


def parse(file):

    data_train = pd.read_csv('Grocery_UPC_Database (sample).csv').dropna(how='any')

    #Depending on the file format, the pd...read will change...for example, excel can be read as pd.read_xls
    # OR if any of the files are compressed...then you can read it like this
    #pd.read_csv(filename.tar.gz, compression='gzip' )
    #some options for compression parameter are {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default ‘infer’
    #refer https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_excel.html#pandas.read_excel



    log = Logger('Report.txt')

    for x, v in enumerate(data_train.columns.values.tolist()):
        uni = data_train[v].unique()  # unique value from each column
        array = data_train[v]  # all element of all column
        ct = pd.crosstab(array, columns="count").sort_values('count', ascending=False)  # count of all unique element in all column
        print("ML Coord is able to read the dataset")

        log.writeLog('Report for Column: {}'.format(v))
        log.writeLog(data_train[v].describe(), False)
        log.writeLog("\n\n ", False)
        log.writeLog("-" * 80, False)

        log.writeLog('\nUnique Values: {}'.format(len(uni)), False)

        log.writeLog("\nTop Values", False)
        log.writeLog(ct.head(5), False)

        log.writeLog("\nBottom Values", False)
        log.writeLog(ct.tail(5), False)

        log.writeLog("-"*80, False)
        log.writeLog("\n\n", False)
        if len(uni) < 250:
            sns.set_context("paper", rc={"font.size":24,"axes.titlesize":24,"axes.labelsize":24})
            f, ax = plt.subplots(figsize=(50, 25))
            sns.set(style="whitegrid", color_codes=True)
            p = sns.countplot(x=v, data=data_train)
            p.set_xlabel("X Label",fontsize=30)
            plt.xticks(rotation=90)
            p.figure.savefig("plot/"+v+".png")

        print("Column Usage Accepted")
        return True