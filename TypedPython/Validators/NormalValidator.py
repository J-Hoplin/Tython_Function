import inspect
from typing import Any
from collections import Counter
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
            self.type = Mode.TYPE_ARGS

        # If type kwargs
        elif self.individualTypes.keys():
            self.type = Mode.TYPE_KWARGS
        # If not -> None
        else:
            self.type = Mode.TYPE_NONE


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

            # Get list of function parameter list
            function_arguments = list(
                filter(
                    lambda x: x not in argkwg_filter,
                    list(
                        map(
                            lambda x: x,
                            list(
                                parameter_info.parameters)))))

            function_arguments = function_arguments if not self.isMethod else function_arguments[1:]
            # get parameter list with default value
            nullable_param = self.getParameterListWithDefaultDictionary(parameter_info)
            # get parameter that is required
            not_nullable_param = list(set(function_arguments).difference(set(nullable_param)))
            # Slice index : to seperate kwargs check range
            slice_index = None
            # Copy args for checking
            args_cpy = args[:] if not self.isMethod else args[1:]
            # for if it's instance
            instance = None if not self.isMethod else args[0]

            # Deprecate Afterward
            # # Case if it's class
            # if self.isMethod:
            #     instance = args_cpy[0]
            #     args_cpy = args_cpy[1:]
            #     function_arguments = function_arguments[1:]

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
                # Some arguments given as kwargs
                kwargs_key_in_parameter = list(
                    filter(
                        lambda x: x in function_arguments, kwargs.keys()))
                '''
                //// check args type parameters ////
                '''
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
                        # params = params[:len(function_arguments)]
                        validation_capsule = list(zip(self.validationTypes,args_cpy[:len(function_arguments)]))
                        print(validation_capsule)
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
                    kwargs_key_in_parameter = list(
                        filter(
                            lambda x: x in valid_function_param,kwargs_key_in_parameter))
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
                # Validate key integration
                for i in self.individualTypes.keys():
                    if i not in function_arguments:
                        raise KwargsIntegrityBrokenException(function.__name__,i)

                # Some arguments in kwargs
                kwargs_key_in_parameter = list(
                    filter(
                        lambda x: x in function_arguments, kwargs.keys()))

                # If strict mode
                if self.strictCheck:
                    # if decorator defined key and function argument not matched
                    if not (Counter(self.individualTypes.keys()) == Counter(function_arguments)):
                        raise KwargsParameterUnmatchedException(function.__name__)

                    # Convert dictionary type defined to sequence type for order vouch
                    iterativeDefine = list(
                        map(
                            lambda x: self.individualTypes[x], function_arguments))

                    # Validation Capsule
                    validation_capsule = list()

                    # Parameter lists
                    params = function_arguments[:]

                    # < Decide Validation >
                    # If argument count is longer than function argument
                    if len(args_cpy) > len(function_arguments):
                        validation_capsule = list(zip(iterativeDefine,args_cpy[:len(function_arguments)]))
                    # If argument count is shorter than function argument
                    else:
                        validation_capsule.extend(list(zip(iterativeDefine[:args_cpy],args_cpy)))
                        getIndexOfKwargsParameter = list(
                            map(
                                lambda x: [x,function_arguments.index(x)],kwargs_key_in_parameter))

                        for key,index in getIndexOfKwargsParameter:
                            validation_capsule.append([iterativeDefine[index],kwargs[key]])

                        # Make smaller scope of validation : except args
                        params = params[len(args_cpy):]

                        # Check if parameter exist as key in kwargs
                        params = list(
                            filter(
                                lambda x: x not in kwargs_key_in_parameter, params))
                        # Check if parameter is nullable type(having default value)
                        params = list(
                            filter(
                                lambda x: x not in nullable_param, params))
                        # If some attribute left -> some value not typed
                        if params:
                            raise UnableToCheckRequiredFieldException(self.modename, function.__name__)
                    validateVardictArgumentDefinition()
                    self.validation(validation_capsule)

                # If not strict mode
                else:
                    validation_capsule = list()
                    convertKeyWithIndex = dict(
                        map(
                            lambda x:(x,[self.individualTypes[x],function_arguments.index(x)]),self.individualTypes.keys()))

                    #filter kwargs ket in parameter only decorator defined
                    kwargs_key_in_parameter = list(
                        filter(
                            lambda x:x in self.individualTypes.keys(),kwargs_key_in_parameter))




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
        return wrapper


