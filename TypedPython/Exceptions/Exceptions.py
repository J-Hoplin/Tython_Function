from TypedPython.Modes.mode import Mode

class ArgumentsNotDefined(Exception):

    def __init__(self,functionname:str,arguments:list):
        super().__init__(f"Some arguments are required in funtion '{functionname}' : {','.join(arguments)}")

class ConfigurationOptionNotSupported(Exception):
    __ConfigLists = [Mode.DEBUG,Mode.PRODUCTION]
    def __init__(self,option):
        super().__init__(f"Configuration option '{option}' not supported\n- Supported types : {', '.join(ConfigurationOptionNotSupported.__ConfigLists)}\n- Debug : Print warning / success message at console\n- Production : Do not print any warning / success message at console")

'''
//// kwargs ////
'''

class KwargsParameterUnmatchedException(Exception):
    def __init__(self,functionname,lostcount):
        super().__init__(f"Some keys defined in decorator are not in parameter list of function '{functionname}' : missing {lostcount} arguments")

class KwargsIntegrityBrokenException(Exception):
    '''
    Exception while : TypeValidation
    For kwargs key not in funciton args
    '''
    def __init__(self,funcname,value):
        super().__init__(f"Unable to find argument '{value}' in function '{funcname}'")

class KwargsUndefinedException(Exception):
    '''
    Exception while : Typevalidation
    For Kwargs matching
    '''
    def __init__(self,funcname,lackBucket):
        super().__init__(f"Arguments not defined in decorator of function {funcname} : {lackBucket}")

'''
//// parameter ////
'''
from TypedPython.Modes.mode import Mode

class ParameterDefinitionCounterUnmatchedException(Exception):
    '''
    Exception while : TypeValidation
    For parameter count unmatched
    '''
    def __init__(self,mode,require,valued):
        if mode == Mode.STRICT:
            self.msg = f"{mode} : Parameter definition count unmatch exception, required : {require} valued : {valued}"
        else:
            self.msg = f"{mode} : Parameter definition count unmatch exception, required at least : {require} valued : {valued}"
        super().__init__(self.msg)


class UnableToCheckRequiredFieldException(Exception):

    def __init__(self,mode,functionname,require_parameters=None):
        if mode == Mode.STRICT:
            self.msg = f"{mode} : Some required parameter field were not given in function '{functionname}'"
        else:
            self.msg = f"{mode} : Some parameters require to check were not given in function '{functionname}'\nRequire Parameter : {','.join(require_parameters)}"
        super().__init__(self.msg)

class ParameterTypeUnmatchedException(Exception):
    '''
    Exception while : TypeValidation
    For parameter type unmatched
    '''
    def __init__(self,require,valued):
        super().__init__(f"Parameter type unmatched exception, required-type : {require} valued-type(value) : {type(valued)}({valued})")

'''
//// Validator ////
'''
class ValidatorTypeInvalid(Exception):
    '''
    Exception while : Type Validation
    For parameter type unmatched
    '''
    def __init__(self):
        super().__init__("Unable to judge validator type. Please use iterative type or hashable type")

class VardictArgmentNotDefined(Exception):
    def __init__(self,argname,functionname):
        super().__init__(f"Variadic argument type '{argname}' not declared but give as input in function '{functionname}'")