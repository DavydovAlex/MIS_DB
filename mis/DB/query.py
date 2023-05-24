import os


class Query:
    __query_extension = 'sql'
    __params_extension = 'txt'

    def __init__(self, name, query, params={}):
        self._query = query
        self._parameters = params
        self._name = name

    @property
    def query(self):
        return self._query

    @property
    def parameters(self):
        return self._parameters

    @property
    def name(self):
        return self._name

    def save(self, folder):
        parametes_path = os.path.join(folder, self._name + '.' + self.__params_extension)
        query_path = os.path.join(folder, self._name + '.' + self.__query_extension)
        if os.path.exists(query_path) or os.path.exists(parametes_path):
            raise FileExistsError
        else:
            with open(query_path, 'w') as f:
                f.write(self._query)
            with open(parametes_path, 'w') as f:
                for key in self._parameters:
                    f.write(str(key) + ': ' + str(self._parameters[key]) + '\n')

    @classmethod
    def load(cls, folder, name):
        parametes_path = os.path.join(folder, name + '.' + cls.__params_extension)
        query_path = os.path.join(folder, name + '.' + cls.__query_extension)
        with open(query_path, 'r',encoding='utf-8-sig') as query_file, open(parametes_path, 'r',encoding='utf-8-sig') as params_file:
            query = query_file.read()
            parameters = {line.split(':')[0]: line.split(':')[1].strip() for line in params_file.readlines()}
            return Query(name, query, parameters)
