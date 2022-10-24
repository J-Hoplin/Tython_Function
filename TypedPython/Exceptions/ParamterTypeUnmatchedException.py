class ParamterTypeUnmatchedException(Exception):
    '''
    Exception while : TypeValidation
    For parameter type unmatched
    '''
    def __int__(self,require,valued):
        super().__init__(f"Parameter type unmatched exception, required-type : {type(require)} valued-type(value) : {type(valued)}({valued})")