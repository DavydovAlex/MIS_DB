import abc
import copy
import pandas as pd
from .filters import *

class FileHandler(abc.ABC):

    @abc.abstractmethod
    def read(self, params: FilterInterface):
        pass

    @abc.abstractmethod
    def write(self, data, params: FilterInterface):
        pass

class ExcelHandler(FileHandler):
    def __init__(self):
        pass

    @staticmethod
    def read(params: FilterInterface):
        if isinstance(params.sheet_name, list):
            data = []
            for page in params.sheet_name:
                page_params = copy.copy(params)
                page_params.sheet_name = page
                df = ExcelHandler.read_page(page_params)
                data.append(df)
            if params.join_pages:
                return ExcelHandler.join_pages(data)
            else:
                return data
        elif isinstance(params.sheet_name, int):
            return ExcelHandler.read_page(params)

    @staticmethod
    def join_pages(pages_data):
        if len(pages_data) > 1:
            df = pages_data[0]
            for i in range(1, len(pages_data)):
                df = pd.concat([df, pages_data[i]])
            return df
        elif len(pages_data) == 1:
            if isinstance(pages_data, list):
                return pages_data[0]
            else:
                return pages_data

    @staticmethod
    def read_page(params: FilterInterface):
        df = pd.read_excel(params.filepath,
                           sheet_name=params.sheet_name,
                           header=params.header,
                           dtype=params.dtype
                           )
        return df

    @staticmethod
    def _get_writer(params: FilterInterface):
        return pd.ExcelWriter(path=params.filepath,
                            date_format=params.date_format,
                            datetime_format=params.datetime_format
                            )

    @staticmethod
    def write(data, params: FilterInterface):
        chunks = ExcelHandler.split_data(data, params.chunk_size)
        writer = ExcelHandler._get_writer(params)
        for i, chunk in enumerate(chunks):
            sheet_name = params.sheet_name + str(i+1)
            page_params = copy.copy(params)
            page_params.sheet_name = sheet_name
            ExcelHandler.write_page(chunk, writer, page_params)
        writer.close()

    @staticmethod
    def write_page_replace(data, params: FilterInterface):
        writer = ExcelHandler._get_writer(params)
        ExcelHandler.write_page(data, writer, params)
        writer.close()

    @staticmethod
    def write_page(data, writer: pd.ExcelWriter, params: FilterInterface):
        data.to_excel(writer,
                      sheet_name=params.sheet_name,
                      header=params.header,
                      na_rep=params.na_rep,
                      index=params.index
                      )

    @staticmethod
    def split_data(data: pd.DataFrame, chunk_size):
        if chunk_size > len(data):
            return [data]
        needed_pages_to_save = len(data)//chunk_size + 1
        chunks = []
        for page in range(needed_pages_to_save):
            chunks.append(data[page*chunk_size:(page+1)*chunk_size])
        return chunks

class CsvHandler(FileHandler):

    @staticmethod
    def read(params: FilterInterface):
        pd_data = pd.read_csv(params.filepath,
                              header=params.header,
                              sep=params.sep,
                              encoding=params.encoding,
                              na_values=params.na_values
                              )
        return pd_data

    @staticmethod
    def write(data, params: FilterInterface):
        data.to_csv(path_or_buf=params.filepath,
                    sep=params.sep,
                    na_rep=params.na_rep,
                    encoding=params.encoding,
                    index=params.index
                    )

    @staticmethod
    def append(data, params: FilterInterface):
        data.to_csv(path_or_buf=params.filepath,
                    sep=params.sep,
                    na_rep=params.na_rep,
                    encoding=params.encoding,
                    index=params.index,
                    header=False,
                    mode='a'
                    )
