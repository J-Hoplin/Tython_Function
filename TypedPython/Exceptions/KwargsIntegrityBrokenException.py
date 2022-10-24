class KwargsIntegrityBrokenException(Exception):
    '''
    Exception while : TypeValidation
    For kwargs key not in funciton args
    '''
    def __init__(self,funcname,value):
        super().__init__(f"Unable to find argument '{value}' in function '{funcname}'")