from typing import List, Union, Any


class DotDict(dict):

    def __repr__(self):
        return f"<DotDict:{super().__repr__()}>"

    @staticmethod
    def load_list(data: List[Any]) -> List[Union['DotDict', List['DotDict'], Any]]:
        result = []
        for d in data:
            if type(d) is dict:
                result.append(DotDict(d))
            elif type(d) is list:
                result.append(DotDict.load_list(d))
            else:
                result.append(d)
        return result

    def __init__(self, *args, **kwargs):
        _rargs = list(args)
        for i in range(0, len(_rargs)):
            if type(_rargs[i]) is dict:
                for key in _rargs[i].keys():
                    if type(_rargs[i][key]) is dict:
                        _rargs[i][key] = DotDict(_rargs[i][key])
                    elif type(_rargs[i][key]) is list:
                        _rargs[i][key] = DotDict.load_list(_rargs[i][key])

        for key in kwargs.keys():
            if type(kwargs[key]) is dict:
                kwargs[key] = DotDict(kwargs[key])

        super().__init__(*tuple(_rargs), **kwargs)

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
