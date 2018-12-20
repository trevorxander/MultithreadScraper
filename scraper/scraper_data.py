import os
import queue
class UrlList:

    _BUFFER_SIZE = 5000

    def __init__(self, url_file_loc):
        self._buffer = queue.Queue(maxsize= UrlList._BUFFER_SIZE)
        self._file = open(url_file_loc, 'r+')

    def __iter__(self):
        return self

    def __next__ (self):
        if self._buffer.empty():
            self._reload_buffer()
        new_url = self._buffer.get()
        return new_url

    def _reload_buffer (self):
        for line in self._file:
            if self._buffer.full():
                break
            self._buffer.put(line.strip())

        if self._buffer.empty():
            raise StopIteration





class PageData:

    def __init__(self, url, file_loc):
        print('test pritn from scraper_data.py')




