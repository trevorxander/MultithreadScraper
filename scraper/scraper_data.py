class UrlList:


    _BUFFER_SIZE = 500

    def __init__(self, url_file_loc):
        self._buffer = [""] * UrlList._BUFFER_SIZE
        self._next_url: str
        self._next_url_index: int
        self.max_urls = UrlList._BUFFER_SIZE

        self._file = open(url_file_loc, 'r')
        self._reload_buffer()

    @property
    def next_url (self):
        if self._next_url_index > self.max_urls - 1:
            self._reload_buffer()

        new_url = self._buffer[self._next_url_index]
        self._next_url_index += 1
        return new_url



    def _reload_buffer (self):
        self._next_url_index = 0


        for url_num in range (0, UrlList._BUFFER_SIZE):
            self._buffer[url_num] = self._file.readline().strip()



class PageData:

    def __init__(self, url, file_loc):
        print('test pritn from url_data.py')




