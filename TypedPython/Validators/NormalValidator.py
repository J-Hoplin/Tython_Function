import inspect,collections,abc
from typing import Any
from TypedPython.Modes.mode import Mode
from TypedPython.Validators.Validation import Validation
from TypedPython.Exceptions.Exceptions import *

class NormalValidator(Validation):
    def __init__(self, *args, strictCheck: bool = True, isTypeMethod=False, **kwargs):
        self.isMethod = isTypeMethod
        self.strictCheck = strictCheck
        self.modename = Mode.STRICT if self.strictCheck else Mode.NON_STRICT
        self.validationTypes = args
        self.individualTypes = kwargs

        # If both types were given, type decision may broken -> raise error
        if self.validationTypes and self.individualTypes:
            raise ValidatorTypeInvalid()

        # If type args
        if self.validationTypes:
            self.type = 'args'

        # If type kwargs
        elif self.individualTypes.keys():
            self.type = 'kwargs'
        # If not -> None
        else:
            self.type = 'none'


    def __call__(self, function):
        def wrapper(*args,**kwargs):
            '''
            ///////////////////////////
            function data preprocessing
            ///////////////////////////
            '''
            # function's args variable
            f_args = inspect.getfullargspec(function).varargs
            # function's kwargs variable
            f_kwargs = inspect.getfullargspec(function).varkw
            # Get variable of args, kwargs variable name
            argkwg_filter = list(
                filter(
                    lambda x: x,[f_args,f_kwargs]))
            #Checkable parameters
            parameter_info = inspect.signature(function)
            # 딕셔너리에 대해 순회를 돌면 기본적으로 키값을 반환하는 성질 활용
            #함수의 매개변수 목록들 추출
            function_arguments = list(
                filter(
                    lambda x: x not in argkwg_filter,
                    list(
                        map(
                            lambda x: x,
                            list(
                                parameter_info.parameters)))))
            # get parameter list with default value
            nullable_param = self.getParameterListWithDefaultDictionary(parameter_info)
            # get parameter that is required
            not_nullable_param = list(set(function_arguments).difference(set(nullable_param)))
            # for if it's instance
            instance = None
            # Slice index : to seperate kwargs check range
            slice_index = None
            # Copy args for checking
            args_cpy = args[:]
            # Case if it's class
            if self.isMethod:
                instance = args_cpy[0]
                args_cpy = args_cpy[1:]
            '''
            ///////////////////////////
            function data preprocessing
            ///////////////////////////
            '''

            '''
            검증 순서
            
            만약 유추된 type이 None인 경우에는 not_nullable_param이 존재하는지 확인한다.
            
            < strict mode > 
            만약 없다면, 그대로 반환하고 만약 있는경우에는, 예외를 발생한다.
            < non strict mode > 
            만약 있다면, 해당 값들을 모두 Any로 포팅한다.
            
            type_args
            
            - 각 필드와 타입을 매핑한다.(function_argument, self.validationType)
            - 우선 입력된 개수를 파악한다
                - 주어진 입력 개수가 type_args에 입력된 수와 동일하다면, 문제없이 진행
                - 개수가 더 적다면 기본값 필드가 정의된 필드인지 확인한다. 아니라면 예외 발생
                - 개수가 더 많다면, *args필드가 정의되었는지 확인한다. 만약 정의되어있지 않다면, 예외 발생
                - validation 실행
            
            type_kwargs
            - 입력된 매개변수들을 필드별로 매핑한다.(function_argument, [])
            - 우선 입력된 개수를 파악한다
                - 데코레이터 필드에 정의된 키들이 함수의 매개변수들(function_argument)과 동일하다면 문제없이 진행
                - 개수가 더 적다면 기본값 필드가 정의된 필드인지 확인한다. 아니라면 예외 발생
                - 데코레이터 필드에 정의된 키들과 매개변수에 입력된 키들이 
            '''

            '''
            /////////////////////////
            some validation functions
            /////////////////////////
            '''

            def validateVardictArgumentDefinition():
                # Check varradict argument(args, kwargs)
                # args checking : after variable of function parameter field
                check_args = args_cpy[len(function_arguments):]
                # if function don't have args variable declaration
                # but over argument found
                if not f_args and check_args:
                    raise VardictArgmentNotDefined('args', function.__name__)
                check_kwargs = list(
                    filter(
                        lambda x: x not in function_arguments,
                        kwargs
                    )
                )
                # kwargs checking
                if not f_kwargs and check_kwargs:
                    raise VardictArgmentNotDefined('kwargs', function.__name__)

            def type_none():
                # If field with not nullable exist
                if not_nullable_param:
                    raise ArgumentsNotDefined(function.__name__, not_nullable_param)
                validateVardictArgumentDefinition()


            def type_Args():
                '''
                //// check args type parameters ////
                '''
                # Some arguments in kwargs
                kwargs_key_in_parameter = list(
                    filter(
                        lambda x: x in function_arguments, kwargs.keys()))
                # If strict mode
                if self.strictCheck:
                    # If length of function argument, validationtype valued length different
                    if len(self.validationTypes) != len(function_arguments):
                        raise ParameterDefinitionCounterUnmatchedException(self.modename,len(function_arguments),len(self.validationTypes))

                    validation_capsule = list()
                    # Check untyped variables

                    params = function_arguments[:]
                    # if args give much more than normal function argument
                    if len(args_cpy) > len(function_arguments):
                        #params = params[:len(function_arguments)]
                        validation_capsule = list(zip(self.validationTypes,params))
                    else:
                        #params = params[:len(function_arguments)]
                        # args type type validate capsule builder
                        # < Decide Validation >
                        validation_capsule.extend(list(zip(self.validationTypes[:len(args_cpy)],args_cpy)))
                        # Filter index of parameter

                        # kwargs type validate capsule builder
                        # value : [key,index of key]
                        getIndexOfKwargsParameter = list(
                            map(
                                lambda x: [x,function_arguments.index(x)],kwargs_key_in_parameter))

                        for key, index in getIndexOfKwargsParameter:
                            validation_capsule.append([self.validationTypes[index],kwargs[key]])

                        # Make smaller scope of validation : except args
                        params = params[len(args_cpy):]

                        # Check if parameter exist as key in kwargs
                        params = list(
                            filter(
                                lambda x:x not in kwargs_key_in_parameter,params))
                        # Check if parameter is nullable type(having default value)
                        params = list(
                            filter(
                                lambda x:x not in nullable_param,params))
                        # If some attribute left -> some value not typed
                        if params:
                            raise UnableToCheckRequiredFieldException(self.modename,function.__name__)

                    validateVardictArgumentDefinition()
                    self.validation(validation_capsule)

                # If non-strict mode : at least required field
                else:
                    validation_capsule = list()
                    # slice in length of function_argument

                    # Function parameter list that should be check : instead of function_argument
                    valid_function_param = function_arguments[:len(self.validationTypes)]
                    kwargs_key_in_parameter = list(filter(lambda x: x in valid_function_param,kwargs_key_in_parameter))
                    # < Decide Validation >
                    # Copy in lentgth of defined validation
                    range_args_cpy = args_cpy[:len(self.validationTypes)]
                    # If have same range or over range
                    if len(self.validationTypes) == len(range_args_cpy):
                        validation_capsule.extend(list(zip(self.validationTypes,range_args_cpy)))
                    # If have args has smaller range
                    else:
                        valid_function_param = valid_function_param[len(range_args_cpy):]
                        validation_capsule.extend(list(zip(self.validationTypes[:len(range_args_cpy)],range_args_cpy)))
                        # kwargs type validate capsule builder
                        # value : [key,index of key]
                        getIndexOfKwargsParameter = list(
                            map(lambda x:[x,function_arguments.index(x)],kwargs_key_in_parameter))
                        print(getIndexOfKwargsParameter)
                        for key,index in getIndexOfKwargsParameter:
                            validation_capsule.append([self.validationTypes[index],kwargs[key]])

                        # If parameter in kwargs
                        valid_function_param = list(
                            filter(
                                lambda x: x not in kwargs_key_in_parameter,valid_function_param))

                        # If parameter in nullable
                        valid_function_param = list(
                            filter(
                                lambda x: x not in nullable_param,valid_function_param))

                        # If some attribute left -> some value not typed
                        if valid_function_param:
                            raise UnableToCheckRequiredFieldException(self.modename,function.__name__,function_arguments[:len(self.validationTypes)])


            def type_Kwargs():
                validateVardictArgumentDefinition()
                '''
                //// check kwargs type parameters  ////
                '''


            by_type = {
                'none' : type_none,
                'args' : type_Args,
                'kwargs' : type_Kwargs
            }
            by_type[self.type]()

            return function(instance, *args, **kwargs) if self.isMethod else function(*args, **kwargs)
            # slice_index = len(args_cpy)
            # # If length of args checking range is more than self.validationtypes
            # if len(self.validationTypes) < len(args_cpy):
            #     check_in_kwargs = function_arguments[len(args_cpy) - len(self.validationTypes): len(args_cpy)]
            #     print(check_in_kwargs)
            #
            # # Make validation : Args
            # self.validation(zip(self.validationTypes[:slice_index], args_cpy[:slice_index]))
            # '''
            # //// check kwargs type parameters  ////
            # '''
            # # Remain field to check
            # function_arguments = function_arguments[slice_index:]
            # # Capsule list for validation : list[type,value]
            # validation_capsule = []
            # # Loop : arguemnt list which require to check type
            # for i in function_arguments:
            #     # If key not in kwargs field
            #     if i not in kwargs.keys():
            #         # Not in kwags field but in group of parameter which has default value -> pass
            #         # Don't make any checking task about parameter with default value
            #         if i in nullable_param:
            #             print(nullable_param)
            #             continue
            #         # If parameter not in both group -> Make exception
            #         raise KwargsIntegrityBrokenException(function.__name__,i)
            #     # Build validation capsule
            #     try:
            #         validation_capsule.append([self.individualTypes[i],kwargs[i]])
            #     except KeyError:
            #         raise KwargsUndefinedException()
            # print(validation_capsule)
            # # Make a validation : kwargs
            # self.validation(validation_capsule)
        return wrapper


