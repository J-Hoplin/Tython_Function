import inspect
from collections import Counter
from TypedPython.Modes.mode import Mode
from TypedPython.Modes.field import Field
from TypedPython.Validators.Validation import Validation
from TypedPython.Exceptions.Exceptions import *
from TypedPython.Modes.MSGS import MSGS

class parameter_validator(Validation):
    def __init__(self, *args, strict_check: bool = True, is_type_method=False, **kwargs):
        super(parameter_validator, self).__init__()
        self.isMethod = is_type_method
        self.strictCheck = strict_check
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
            nullable_param = self.get_parameter_list_with_default_dictionary(parameter_info)
            # get parameter that is required
            not_nullable_param = list(set(function_arguments).difference(set(nullable_param)))
            # # If it's method remove 'self' from not nullable param

            # if self.isMethod:
            #     not_nullable_param.remove(function_arguments[0])

            # Slice index : to seperate kwargs check range
            slice_index = None
            # Copy args for checking
            args_cpy = args[:] if not self.isMethod else args[1:]
            # for if it's instance
            instance = None if not self.isMethod else args[0]

            '''
            ////////////////////////////
            Validation & Integrity Check
            ////////////////////////////
            '''
            # ARGS Type validation
            if self.type == Mode.TYPE_ARGS:
                # Integrity validate required in both strict / non-strict
                if len(self.validationTypes) > len(function_arguments):
                    raise ParameterDefinitionCounterUnmatchedException(self.modename,len(function_arguments),len(self.validationTypes))

                # Strict Mode
                if self.strictCheck:
                    # If types defined in decorator count not match with function parameter count
                    if len(self.validationTypes) != len(function_arguments):
                        raise ParameterDefinitionCounterUnmatchedException(self.modename, len(function_arguments), len(self.validationTypes))

            # Kwargs Type validation
            if self.type == Mode.TYPE_KWARGS:
                # Key integration validate required in both strict / non-strict
                for i in self.individualTypes.keys():
                    if i not in function_arguments:
                        raise KwargsIntegrityBrokenException(function.__name__, i)
                # Strict Mode
                if self.strictCheck:
                    # If types defined in decorator not match with function parameter
                    if not (Counter(self.individualTypes.keys()) == Counter(function_arguments)):
                        raise KwargsParameterUnmatchedException(function.__name__,len(
                            list(
                                filter(
                                    lambda x: x not in self.individualTypes.keys(),function_arguments))))


            # Deprecate Afterward
            # # Case if it's class
            # if self.isMethod:
            #     instance = args_cpy[0]
            #     args_cpy = args_cpy[1:]
            #     function_arguments = function_arguments[1:]

            # Pre process dictionary for function_Preprocess
            for i,v in enumerate(function_arguments):
                capsule = dict()
                # Field index
                capsule[Field.INDEX] = i
                if self.type == Mode.TYPE_ARGS:
                    # Nullable check field
                    capsule[Field.NULLABLE] = True if v in nullable_param else False
                    # Map Type
                    try:
                        capsule[Field.TYPE] = self.validationTypes[i]
                    except IndexError:
                        capsule[Field.TYPE] = object
                elif self.type == Mode.TYPE_KWARGS:
                    capsule[Field.NULLABLE] = True if v in nullable_param else False
                    try:
                        capsule[Field.TYPE] = self.individualTypes[v]
                    except KeyError:
                        continue
                self.parameter_Preprocess[v] = capsule


            '''
            /////////////////////////
            some validation functions
            /////////////////////////
            '''

            def validate_vardict_argument_definition():
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
                validate_vardict_argument_definition()
                if self._level == Mode.DEBUG:
                    if not_nullable_param:
                        MSGS.warning_nonsafe(function.__name__,len(not_nullable_param),len(not_nullable_param))
                    else:
                        MSGS.success_successmsg(function.__name__)

            def type_args():

                # Some arguments given as kwargs
                kwargs_key_in_parameter = list(
                    filter(
                        lambda x: x in function_arguments, kwargs.keys()))
                '''
                //// check args type parameters ////
                '''
                validation_capsule = list()
                # If strict mode
                if self.strictCheck:
                    # Check untyped variables
                    params = function_arguments[:]
                    # if args give much more than normal function argument
                    if len(args_cpy) >= len(function_arguments):
                        # params = params[:len(function_arguments)]
                        validation_capsule = list(zip(self.validationTypes,args_cpy[:len(function_arguments)]))
                    else:
                        if (len(kwargs_key_in_parameter) + len(args_cpy)) != len(function_arguments):
                            # Check if not given values is nullable field
                            if Counter(function_arguments[(len(args_cpy) + len(kwargs_key_in_parameter)):]) != Counter(nullable_param):
                                raise UnableToCheckRequiredFieldException(self.modename, function.__name__)

                        # args type type validate capsule builder
                        # < Decide Validation >
                        validation_capsule.extend(list(zip(self.validationTypes[:len(args_cpy)],args_cpy)))
                        # Filter index of parameter
                        # kwargs type validate capsule builder
                        # value : [key,index of key]
                        getIndexOfKwargsParameter = list(
                            map(
                                lambda x: [x,self.parameter_Preprocess[x][Field.TYPE]],kwargs_key_in_parameter))

                        for key, type in getIndexOfKwargsParameter:
                            validation_capsule.append([type,kwargs[key]])

                # If non-strict mode : at least required field
                else:
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
                        if len(range_args_cpy) + len(kwargs_key_in_parameter) != len(self.validationTypes):
                            raise UnableToCheckRequiredFieldException(self.modename, function.__name__,function_arguments[:len(self.validationTypes)])

                        valid_function_param = valid_function_param[len(range_args_cpy):]
                        validation_capsule.extend(
                            list(
                                zip(self.validationTypes[:len(range_args_cpy)],range_args_cpy)))
                        # kwargs type validate capsule builder
                        # value : [key,index of key]
                        getIndexOfKwargsParameter = list(
                            map(
                                lambda x:[x,self.parameter_Preprocess[x][Field.TYPE]],kwargs_key_in_parameter))
                        for key,type in getIndexOfKwargsParameter:
                            validation_capsule.append([type,kwargs[key]])

                validate_vardict_argument_definition()
                self.validation(validation_capsule)

                if self._level == Mode.DEBUG:
                    if self.strictCheck:
                        MSGS.success_successmsg(function.__name__)
                    else:
                        # Get count of not nullable but not checking
                        not_nullable_but_not_checked = list(
                            filter(
                                lambda x: x not in valid_function_param,not_nullable_param))
                        if not not_nullable_but_not_checked:
                            MSGS.success_successmsg(function.__name__)
                        else:
                            MSGS.warning_nonsafe(function.__name__,len(not_nullable_param),len(not_nullable_but_not_checked))

            def type_kwargs():
                # Get field list of parameter that exist in kwargs
                kwargs_key_in_parameter = list(
                    filter(
                        lambda x: x in function_arguments, kwargs.keys()))

                # Validation Capsule
                validation_capsule = list()

                # If strict mode
                if self.strictCheck:
                    # Convert dictionary type defined to sequence type for order vouch
                    if len(args_cpy) >= len(function_arguments):
                        range_args_cpy = args_cpy[:len(function_arguments)]
                        validation_capsule.extend(list(
                            map(
                                lambda x:[self.parameter_Preprocess[x][Field.TYPE],
                                          range_args_cpy[self.parameter_Preprocess[x][Field.INDEX]]],
                                self.parameter_Preprocess.keys())))

                    # If argument count is shorter than function argument
                    else:
                        if (len(args_cpy) + len(kwargs_key_in_parameter)) != len(function_arguments):
                            # Check if not given values is nullable field
                            if Counter(function_arguments[(len(args_cpy) + len(kwargs_key_in_parameter)):]) != Counter(nullable_param):
                                raise UnableToCheckRequiredFieldException(self.modename, function.__name__)

                        validation_capsule.extend(list(
                            map(
                                lambda k,v:[self.parameter_Preprocess[k][Field.TYPE],v],zip(function_arguments[:len(args_cpy)],args_cpy))))
                        validation_capsule.extend(list(
                            map(lambda x:[self.parameter_Preprocess[x][Field.TYPE],kwargs[x]],kwargs_key_in_parameter)))

                # If not strict mode
                else:
                    # Get args given parameters
                    range_args_cpy = args_cpy[:len(function_arguments)]
                    # Get field list of parameter that exist in args type
                    parameters_in_args = function_arguments[:len(range_args_cpy)]
                    for k,v in self.individualTypes.items():
                        if k in parameters_in_args:
                            validation_capsule.append([self.parameter_Preprocess[k][Field.TYPE],range_args_cpy[self.parameter_Preprocess[k][Field.INDEX]]])
                        else:
                            validation_capsule.append([self.parameter_Preprocess[k][Field.TYPE],kwargs[k]])

                validate_vardict_argument_definition()
                self.validation(validation_capsule)

                if self._level == Mode.DEBUG:
                    if self.strictCheck:
                        MSGS.success_successmsg(function.__name__)
                    else:
                        not_nullable_but_not_checked = list(
                            filter(
                                lambda x: x not in self.parameter_Preprocess.keys(),not_nullable_param))
                        if not not_nullable_but_not_checked:
                            MSGS.success_successmsg(function.__name__)
                        else:
                            MSGS.warning_nonsafe(function.__name__, len(not_nullable_param),len(not_nullable_but_not_checked))

                '''
                //// check kwargs type parameters  ////
                '''
            by_type = {
                'none' : type_none,
                'args' : type_args,
                'kwargs' : type_kwargs
            }
            by_type[self.type]()
            return function(*args, **kwargs)
        return wrapper
