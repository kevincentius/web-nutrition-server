
class Response:
    def __init__(self, labels):
        self.dict = {}
        for name, label in labels.items():
            if label is None:
                self.dict[name] = LabelError().dict
            else:
                self.dict[name] = label.dict


class Label:
    def __init__(self, main_score=None, subfeatures=None, status='ok'):
        self.dict = {
            'status': status
        }

        if main_score is not None:
            self.dict['main_score'] = main_score
        if subfeatures is not None:
            sf_array = []
            for subfeature in subfeatures:
                sf_array.append(subfeature.dict)

            self.dict['subfeatures'] = sf_array


class LabelError(Label):
    def __init__(self):
        Label.__init__(self, status='error')


class SubFeature:
    def __init__(self, name, value=None, percentage=None, status='ok', tooltip=None):
        self.dict = {
            'status': status,
            'name': name
        }

        if value is not None:
            self.dict['value'] = value
            if percentage is None:
                percentage = value
        if percentage is not None:
            self.dict['percentage'] = percentage
        if tooltip is not None:
            self.dict['tooltip'] = tooltip


class SubFeatureError(SubFeature):
    def __init__(self, name):
        SubFeature.__init__(self, name, status='error')
