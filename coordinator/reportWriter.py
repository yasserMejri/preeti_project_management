import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from django.conf import settings

def parse_file(file):
    data_train = pd.read_csv(file).dropna(how='any')

    result_data = []

    print data_train.columns

    rowCount = len(data_train.columns.values.tolist())
    colCount = len(data_train.index)
    for x, v in enumerate(data_train.columns.values.tolist()):
        uni = data_train[v].unique()  # unique value from each column
        array = data_train[v]  # all element of all column
        ct = pd.crosstab(array, columns="count").sort_values('count', ascending=False)  # count of all unique element in all column
        print("ML Coord is able to read the dataset")

        print 'Report for Column: {}'.format(v)
        print data_train[v].describe()
        print '\n\n'
        print '-' * 80
        print '\nUnique Values: {}'.format(len(uni))
        print '\nTop Values'
        print ct.head(5)
        print "\nBottom Values"
        print ct.tail(5)
        print "-"*80
        print "\n\n"

        # print 'TEST DATAFRAME'
        # print ct.iloc[0][0]
        # print ct.iloc[0]
        # print ct.iloc[-1][0]
        # print ct.iloc[-1]
        # print ct.index[0]
        # print '/TEST DATAFRAME'

        result_data.append({
            'column_name': format(v), 
            'unique_values': format(len(uni)), 
            'most_frequent': ct.index[0], 
            'least_frequent': ct.index[-1], 
            })

        # if len(uni) < 250:
        #     sns.set_context("paper", rc={"font.size":24,"axes.titlesize":24,"axes.labelsize":24})
        #     f, ax = plt.subplots(figsize=(50, 25))
        #     sns.set(style="whitegrid", color_codes=True)
        #     p = sns.countplot(x=v, data=data_train)
        #     p.set_xlabel("X Label",fontsize=30)
        #     plt.xticks(rotation=90)
        #     p.figure.savefig(settings.BASE_DIR + "/plot/"+v+".png")

        print "Column Usage Accepted"


    print result_data

    return True, result_data, colCount, rowCount
