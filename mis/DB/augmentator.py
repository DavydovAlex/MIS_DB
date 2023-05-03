import pandas as pd
import numpy as np
from copy import copy
import query


class Augmentator:

    def __init__(self, connection,
                 data: pd.DataFrame,
                 query: query.Query,
                 values_to_add):
        self.connection = connection
        self.data = data[:]
        self.query = query

    def augmentate(self, chunk_size=100):
        data_length = self.data.shape[0]
        for chunk in range(0, data_length, chunk_size):
            chunk_data = self.data[chunk:chunk + chunk_size - 1] if \
                data_length - chunk > chunk_size else self.data[chunk:]
            queries_list = []
            for i in range(0, chunk_size):
                params = {}
                for column in self.query.params:
                    params[column] = chunk_data[self.query.params[column]][i]
                queries_list.append(params)
                print(params)
                # queries_list.append(query.Query(name=i, query=self.query.query, params=params))





if __name__ == '__main__':
    dic = {1: 2, 3: 4}
    print(dic.values())
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(df[0][1])
    for i in range(0, 95, 100):
        print(i)
