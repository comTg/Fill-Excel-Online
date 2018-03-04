class TableInfo(object):
    def __init__(self,id,title,expired):
        self.id = id
        self.title = title
        self.expired = expired

    def set_title(self,title):
        self.title = title

    def get_title(self):
        return self.title

    def set_expired(self,expired):
        self.expired = expired

    def get_expired(self):
        return self.expired