from TypedPython.Exceptions.ParamterTypeUnmatchedException import ParamterTypeUnmatchedException

# Base Validation Class
class BaseValidation(object):
    # define access modifier as protected
    def _validation(self,validationbucket):
        #print(list(validationbucket))
        require = value = None
        for require, value in validationbucket:
            assert type(value) is require or ParamterTypeUnmatchedException(require, value)