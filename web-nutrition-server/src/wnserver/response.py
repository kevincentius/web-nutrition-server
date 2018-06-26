
class Response:
    def __init__(self):
        self.dict = {}

    def add_label(self, name, value):
        if value is None:
            self.dict[name] = {'status': 'error'}
        else:
            value['status'] = 'ok'
            self.dict[name] = value
