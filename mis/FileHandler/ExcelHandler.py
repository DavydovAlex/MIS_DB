import abc

from  openpyxl import Workbook
from abc import ABC

class FileHandler(ABC):
    _path = None
    _header = None

    def __init__(self, path):
        self._path = path

    @property
    def header(self):
        return self._header

    @property
    def path(self):
        return self._path

    def set_header(self, val):
        self._header = val
        return self

    @abc.abstractmethod
    def write(self, iterator):
        pass

class ExcelHandler(FileHandler):
    _sheet_rows = 999999
    def __init__(self, path):
        super().__init__(path)

    @property
    def sheet_rows(self):
        return self._sheet_rows

    def set_sheet_rows(self, val):
        if type(val) != int:
            raise TypeError('Rows number must be int')
        if val >= 1000000:
            raise ValueError('Maximum rows count is 999999')
        self._sheet_rows = val

    def write(self, iterator):
        wb = Workbook()
        ws = wb.active
        rows_in_sheet = 0
        if self.header:
            ws.append(self.header)
            rows_in_sheet = 1
        for row in iterator:
            if rows_in_sheet <= self._sheet_rows:
                ws.append(self.header)
            else:
                rows_in_sheet = 0
                wb.create_sheet()
                ws = wb.active
                if self.header:
                    ws.append(self.header)
                    rows_in_sheet = 1
        wb.save(self.path)








if __name__ == '__main__':
    handler = ExcelHandler('123').set_sheet_rows('11')
    print(handler.header)





