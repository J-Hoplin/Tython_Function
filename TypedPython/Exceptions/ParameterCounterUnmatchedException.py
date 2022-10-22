class ParameterCounterUnmatchedException(Exception):
    '''
    Exception while : TypeValidation
    For parameter count unmatched
    '''
    def __init__(self,require,valued):
        super().__init__(f"Parameter count exception, required : {require} valued : {valued}")