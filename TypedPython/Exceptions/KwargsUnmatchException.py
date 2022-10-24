class KwargsUnmatchException(Exception):
    '''
    Exception while : Typevalidation
    For Kwargs matching
    '''
    def __init__(self,funcname,lackBucket):
        super().__init__(f"Some arguments not defined in decorator of function {funcname} : {lackBucket}")