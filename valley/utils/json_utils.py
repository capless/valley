import json
import inspect

from .imports import import_util


class ValleyEncoder(json.JSONEncoder):
    show_type = True

    def default(self, obj):
        if not isinstance(obj, (list,dict,int,float,bool)):
            if self.show_type:
                obj._data['_type'] = '{}.{}'.format(inspect.getmodule(obj).__name__, obj.__class__.__name__)
            return obj._data
        return super(ValleyEncoder, self).default(obj)


class ValleyEncoderNoType(ValleyEncoder):
    show_type = False


class ValleyDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        klass = import_util(obj['_type'])
        obj.pop('_type')

        return klass(**obj)
