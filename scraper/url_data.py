class UrlList:

    def __init__(self, url_file_loc):
        self.file = open(url_file_loc, 'r')

class PageData:

    def __init__(self, url, file_loc):
        