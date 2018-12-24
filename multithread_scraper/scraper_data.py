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


class PageDataCollection:
    _MAX_PAGE_DATA = 50
    _NULL_WORD = "Not Found"
    mutex = Lock()

    def __init__(self, write_file_loc):
        self._buffer = queue.Queue(maxsize=PageDataCollection._MAX_PAGE_DATA)
        self._file = open(write_file_loc, 'w')

    def __del__(self):
        self._file.close()

    def add_page(self, page_data: dict):
        PageDataCollection.mutex.acquire()
        try:
            self._buffer.put(page_data)
            if self._buffer.full():
                self.flush()
        finally:
            PageDataCollection.mutex.release()

    def flush(self):
        while not self._buffer.empty():
            page_data: dict
            page_data = self._buffer.get()

            for type, data in page_data.items():
                self._file.write(type)
                self._file.write(": ")
                for elem in data:
                    self._file.writelines(elem)
                    self._file.write(" ")
                self._file.write("\n")
            self._file.write('\n----------\n')
