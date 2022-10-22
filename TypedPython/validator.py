from TypedPython.Exceptions.ParameterCounterUnmatchedException import ParameterCounterUnmatchedException
from TypedPython.Exceptions.ParamterTypeUnmatchedException import ParamterTypeUnmatchedException

class TypeValidation(object):
    def __init__(self,*args,forceCount=True,isClass=False):
        self.isClass = isClass
        self.forceCount = forceCount
        self.validationTypes = args

    def __call__(self, function):
        def wrapper(*args):
            instance = None
            slice_index = None
            # Case if it's class
            if self.isClass:
                instance = args[0]
                args = args[1:]
            # if forceCount
            if self.forceCount:
                if len(args) != len(self.validationTypes):
                    raise ParameterCounterUnmatchedException(len(args),len(self.validationTypes))
                else:
                    slice_index = len(self.validationTypes)
            else:
                slice_index = min([len(self.validationTypes),len(args)])
            # Make validation
            self.__validation(zip(self.validationTypes[:slice_index], args[:slice_index]))
            return function(instance,*args) if self.isClass else function(*args)
        return wrapper

    def __validation(self,validationbucket):
        #print(list(validationbucket))
        require = value = None
        try:
            for require, value in validationbucket:
                print(f"{require} {value}")
                assert type(value) is require
        except AssertionError:
            raise ParamterTypeUnmatchedException(type(require),type(value))