import inspect,collections,abc
from TypedPython.Validators.BaseValidator import BaseValidation
from TypedPython.Exceptions.ParameterCounterUnmatchedException import ParameterCounterUnmatchedException
from TypedPython.Exceptions.KwargsIntegrityBrokenException import KwargsIntegrityBrokenException
from TypedPython.Exceptions.KwargsUnmatchException import KwargsUnmatchException

class NormalValidator(BaseValidation):
    def __init__(self,*args,strictCheck:bool=True,isTypeMethod=False,**kwargs):
        self.isMethod = isTypeMethod
        self.strictCheck = strictCheck
        self.validationTypes = args

    def __call__(self, function):
        def wrapper(*args,**kwargs):
            instance = None
            slice_index = None
            '''
            //// check args type parameters ////
            '''
            # Case if it's class
            if self.isMethod:
                instance = args[0]
                args = args[1:]
            # if forceCount
            if self.strictCheck:
                if len(args) != len(self.validationTypes):
                    raise ParameterCounterUnmatchedException(len(args),len(self.validationTypes))
                else:
                    slice_index = len(self.validationTypes)
            # Uncheck force count
            else:
                slice_index = min([len(self.validationTypes),len(args)])
            # Make validation
            self._validation(zip(self.validationTypes[:slice_index], args[:slice_index]))
            return function(instance, *args,**kwargs) if self.isMethod else function(*args,**kwargs)
        return wrapper
