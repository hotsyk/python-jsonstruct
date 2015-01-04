# -*- coding: utf-8 -*-

import json


class Struct(object):

    """ Building recursive storage object """

    def __init__(self, **entries):
        new_data = entries.copy()
        for key in new_data.keys():
            if isinstance(new_data[key], dict):
                new_data[key] = Struct(**new_data[key])
            elif isinstance(new_data[key], list):
                new_data[key] = [
                    Struct(**item) if isinstance(item, dict) else item
                    for item in new_data[key]]
            elif isinstance(new_data[key], tuple):
                new_data[key] = tuple(
                    Struct(**item) if isinstance(item, dict) else item
                    for item in new_data[key])

        self.__dict__.update(new_data)

    def __getattr__(self, key):
        """  __getattr__ to avoid exception when not attr found """
        try:
            return object.__getattr__(self, key)
        except AttributeError:
            # but raise for any missing internal methods
            if key.startswith('_'):
                raise
            return None

    def get_data(self):
        """ Return stored data as dict """
        data = {}
        for field in self.__dict__:
            _field = getattr(self, field, None)
            if isinstance(_field, self.__class__):
                data[field] = _field.get_data()
            elif isinstance(_field, list):
                data[field] = [
                    _f.get_data() if isinstance(_f, self.__class__)
                    else _f for _f in _field]
            else:
                data[field] = _field
        return data

    def get_json(self, data=None):
        if not data:
            data = self.get_data()

        return json.dumps(data)
