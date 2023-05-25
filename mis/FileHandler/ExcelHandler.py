import abc
import sys

from openpyxl import Workbook
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
    MAX_ROWS = 999999
    _sheet_rows = None

    def __init__(self, path):
        super().__init__(path)
        self._sheet_rows = self.MAX_ROWS

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
        wb = Workbook(write_only=True)
        ws = wb.create_sheet()
        #wb.active = len(wb.worksheets) - 1
        rows_in_sheet = 0
        if iterator.header:
            ws.append(iterator.header)
            rows_in_sheet = 1
        for row in iterator:
            if rows_in_sheet % 100000 == 0:
                print(str(rows_in_sheet) + ':' + str(row))
            if rows_in_sheet < self._sheet_rows:
                rows_in_sheet += 1
                ws.append(row)
            else:
                rows_in_sheet = 0
                ws = wb.create_sheet()
                #wb.active = len(wb.worksheets) - 1
                if iterator.header:
                    ws.append(iterator.header)
                    rows_in_sheet = 1
        wb.save(self.path)

    def read_page(self, name=None, order=None, data_start=None):
        pass


if __name__ == '__main__':
    handler = ExcelHandler('123').set_sheet_rows('11')
    print(handler.header)





