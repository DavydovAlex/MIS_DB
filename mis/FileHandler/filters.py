import abc

class FilterInterface(abc.ABC):
    pass


class CsvFilterRead(FilterInterface):
    def __init__(self,
                 filepath,
                 *,
                 encoding='utf-8-sig',
                 sep=';',
                 na_values='',
                 header=None
                 ):
        self._filepath = filepath
        self._encoding = encoding
        self._header = header
        self._sep = sep
        self.na_values = na_values
    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, val):
        self._filepath = val

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, val):
        self._encoding = val

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def sep(self):
        return self._sep

    @sep.setter
    def sep(self, val):
        self._sep = val

    @property
    def na_values(self):
        return self._na_values

    @na_values.setter
    def na_values(self, val):
        self._na_values = val


class CsvFilterWrite(FilterInterface):
    def __init__(self,
                 filepath,
                 *,
                 encoding='utf-8-sig',
                 sep=';',
                 na_rep='null',
                 header=True,
                 index=True
                 ):
        self._filepath = filepath
        self._encoding = encoding
        self._header = header
        self._sep = sep
        self._na_rep = na_rep
        self._index = index

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, val):
        self._filepath = val

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, val):
        self._encoding = val

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def sep(self):
        return self._sep

    @sep.setter
    def sep(self, val):
        self._sep = val

    @property
    def na_rep(self):
        return self._na_rep

    @na_rep.setter
    def na_rep(self, val):
        self._na_rep = val

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val


class ExcelFilterRead(FilterInterface):
    def __init__(self,
                 filepath,
                 sheet_name=0,
                 *,
                 header=None,
                 dtype=None,
                 join_pages=False
                 ):
        self._filepath = filepath
        self._header = header
        self._sheet_name = sheet_name
        self._dtype = dtype
        self._join_pages = join_pages

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, val):
        self._filepath = val

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def sheet_name(self):
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, val):
        self._sheet_name = val

    @property
    def dtype(self):
        return self._dtype

    @property
    def join_pages(self):
        return self._join_pages


class ExcelFilterWrite(FilterInterface):
    def __init__(self,
                 filepath,
                 *,
                 sheet_name='Sheet1',
                 na_rep='',
                 header=True,
                 index=False,
                 chunk_size=999999,
                 date_format='DD.MM.YYYY',
                 datetime_format='DD.MM.YYYY HH:MM:SS',
                 day_first=True
                 ):
        self._filepath = filepath
        self._header = header
        self._sheet_name = sheet_name
        self._index = index
        self._chunk_size = chunk_size
        self._na_rep = na_rep
        self._date_format = date_format
        self._datetime_format = datetime_format
        self._day_first = day_first


    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, val):
        self._filepath = val

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, val):
        self._header = val

    @property
    def sheet_name(self):
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, val):
        self._sheet_name = val

    @property
    def na_rep(self):
        return self._na_rep

    @property
    def index(self):
        return self._index

    @property
    def chunk_size(self):
        return self._chunk_size

    @property
    def date_format(self):
        return self._date_format

    @property
    def datetime_format(self):
        return self._datetime_format

    @property
    def day_first(self):
        return self._day_first