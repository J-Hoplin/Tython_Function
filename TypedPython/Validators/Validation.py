import inspect,abc
from TypedPython.Exceptions.Exceptions import ParameterTypeUnmatchedException

class Validation(object):

    def __init__(self):
        self.parameter_Preprocess = dict()

    def validation(self,validationbucket):
        for require, value in validationbucket:
            # For multiple type utilities (ex : Union)
            if '__args__' in vars(require):
                if not type(value) in vars(require)['__args__']:
                    raise ParameterTypeUnmatchedException(require, value)

            elif not type(value) is require:
                raise ParameterTypeUnmatchedException(require,value)

    def getParameterListWithDefaultDictionary(self,info:inspect.signature):
        return list(
            map(
                lambda x:x.name,
                    list(
                        filter(
                            lambda x: x.name if x.default is not inspect._empty else False,list(info.parameters.values())))))