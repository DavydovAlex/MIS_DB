import pandas as pd
import numpy as np
from copy import copy


class Augmentator:

    def __init__(self, connection,
                 data: pd.DataFrame,
                 query,
                 values_to_add):
        self.connection = connection
        self.data = data[:]
        self.query = query

    def augmentate(self, chunk_size=100):
        data_length = self.data.shape[0]
        for chunk in range(0, data_length, chunk_size):
            chunk_data = self.data[chunk:chunk + chunk_size - 1] if data_length - chunk > chunk_size else self.data[
                                                                                                          chunk:]
            for i in range(0, chunk_size):
                params = {}
                for column in self.query.params:
                    params[column] = chunk_data[self.query.params[column]][i]

    def _select_chunk(self, data):
        pass


if __name__ == '__main__':
    dic = {1: 2, 3: 4}
    print(dic.values())
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(df[0][1])
    for i in range(0, 95, 100):
        print(i)
