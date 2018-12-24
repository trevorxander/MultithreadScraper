import queue
from threading import Lock


class UrlList:
    _BUFFER_SIZE = 5000
    mutex = Lock()

    def __init__(self, url_file_loc):
        self._buffer = queue.Queue(maxsize=UrlList._BUFFER_SIZE)
        self._file = open(url_file_loc, 'r')

    def __iter__(self):
        return self

    def __next__(self):
        UrlList.mutex.acquire()
        try:
            if self._buffer.empty():
                self._reload_buffer()
            new_url = self._buffer.get()
            return new_url
        finally:
            UrlList.mutex.release()

    def _reload_buffer(self):
        for line in self._file:
            if self._buffer.full():
                break
            self._buffer.put(line.strip())

        if self._buffer.empty():
            raise StopIteration


class PageData:
    def __init__(self, ):
        self._data = {}
        self._data_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._data_index > len(self._data) - 1:
            raise StopIteration
        new_data = self._data[self._data_index]
        self._data_index += 1
        return new_data

    def add_data(self, data_desc: str, data: list):
        self._data[data_desc] = data

    def get_data(self, type: str):
        return self._data[type]


class PageDataCollection:
    _MAX_PAGE_DATA = 50
    mutex = Lock()

    def __init__(self, write_file_loc):
        self.key_word_id = 1
        self.website_id = 1
        self._buffer = queue.Queue(maxsize=PageDataCollection._MAX_PAGE_DATA)
        self._file = open(write_file_loc, 'w')

    def __del__(self):
        self._file.close()

    def add_page(self, page_data: PageData):
        PageDataCollection.mutex.acquire()
        try:
            self._buffer.put(page_data)
            if self._buffer.full():
                self.flush()
        finally:
            PageDataCollection.mutex.release()

    def flush(self):
        write_count = 0
        while not self._buffer.empty():
            page_data: PageData
            page_data = self._buffer.get()

            self._file.writelines(page_data._data.get('Title') + ['\n'])
            self._file.writelines(page_data._data.get('URL') + ['\n'])
            self._file.writelines(page_data._data.get('Description') + ['\n'])

            words = page_data._data.get('Words')
            for word in words:
                self._file.write(word + ' ')
            self._file.write('\n----------\n')
