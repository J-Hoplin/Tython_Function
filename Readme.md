Tython Function
===
***
**Tython Function**은 Python의 `Function` 혹은 `Method` Parameter에 대해 Type을 validation 해주는 `Decorator`입니다.앞으로 구현해볼 `Typed Python`에서 함수 부분의 Type Binding 로직입니다.
- 데코레이터가 무엇인지 모르시나요? 아래 링크를 참고해주세요(Don't know about python decorator? Please refer link under below)
    - https://peps.python.org/pep-0318/

Python version 3.7 이상이 권장됩니다.
***
## License Information

<img src="https://opensource.org/files/OSIApproved_1.png" width=75 height=100 align="right" alt="opensource icon">

- [MIT License](https://opensource.org/licenses/MIT)
- Copyright by Hoplin
- Tython Function : Tython Function / Method is Python Decorator for validating parameter input type
***
## Basic Usage - Function

1. Clone project
```bash
git clone https://github.com/J-hoplin1/Tython_Function.git
```
2. Import Decorator Class

```python
from TypedPython.Validators.ParameterValidator import parameter_validator

# Configurate mode(Set default as 'debug') : 'debug' or 'production'
parameter_validator.config('debug')
```

- Validator의 mode를 지정해줄 수 있습니다. Default모드는 `debug` 모드입니다. 만약 Default상태로 사용하고 싶은 경우에는, `config()`함수를 호출할 필요가 없습니다. 모드로는 `debug`, `production` 두가지 모드가 있습니다. 

3. `Function`에 데코레이터 적용해 보기

Validator에는 두가지 타입이 있습니다. `Sequence` 타입과 `Key-Value` 타입, `None`타입 세가지가 있습니다. None타입은 아무것도 검사하지 않는 경우이며, 사용하지 않는경우와 동일합니다.(`None`타입에 대한 설명은 아래 코드에서 마치겠습니다)

```python
#Console
#Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function 'example_function' - Not nullable : 4 / Not checked counter : 4
#10 abc defg [1, 2, 3, 4, 5]
@parameter_validator()
def example_function(a,b,c,d):
    print(a,b,c,d)

example_function(10,'abc','defg',[1,2,3,4,5])
```

그리고 Validator에는 `strictCheck`라는 옵션이 존재합니다. `strictCheck`는 모든 매개변수에 대해 타입을 검사해야하는지의 여부를 결정합니다. `strictCheck`이 `True`인 경우에는 모든 Parameter에 대해 Type을 정의해 주어야 합니다. `strictCheck`의 Default는 `True`입니다

Validator는 파이썬에서 사용할 수 있는 모든 Type을 지원합니다. 혹시라도 Validation이 안되는 타입이 존재한다면 Issue를 남겨주시면 감사하겠습니다.

- Sequence type + strictCheck=True
```python
from typing import Union
import pandas as pd

#Console
#Success to validate parameter types of function 'example_function'
#10 abc [1, 2, 3] Empty DataFrame
#Columns: []
#Index: []

@parameter_validator(int,str,Union[int,str,list],pd.DataFrame)
def example_function(a,b,c,d):
    print(a,b,c,d)

example_function(10,'abc',[1,2,3],pd.DataFrame())
```
- Sequence type + strictCheck=False
```python
from typing import Union

#Console
#Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function 'example_function' - Not nullable : 4 / Not checked counter : 2
#10 abc [1, 2, 3] [10, 11, 12]

@parameter_validator(int,str,strictCheck=False)
def example_function(a,b,c,d):
    print(a,b,c,d)

example_function(10,'abc',[1,2,3],[10,11,12])
```
- Key-Value type + strictCheck=True
```python
from typing import Union

#Console
#Success to validate parameter types of function 'example_function'
#10 abc [1, 2, 3] [10, 11, 12]
@parameter_validator(a=int,c=Union[int,str,list],b=str,d=list)
def example_function(a,b,c,d):
    print(a,b,c,d)

example_function(10,'abc',[1,2,3],[10,11,12])
```
- Key-Value type + strictCheck=False
```python
from typing import Union

# Console : Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function 'example_function' - Not nullable : 4 / Not checked counter : 2
@parameter_validator(a=int,d=Union[int,str,list],strictCheck=False)
def example_function(a,b,c,d):
    print(a,b,c,d)

example_function(10,'abc',[1,2,3],[10,11,12])
```


## Basic Usage - Method

1. Clone project
```bash
git clone https://github.com/J-hoplin1/Tython_Function.git
```
2. Import Decorator Class

```python
from TypedPython.Validators.ParameterValidator import parameter_validator

# Configurate mode(Set default as 'debug') : 'debug' or 'production'
parameter_validator.config('debug')
```

- Validator의 mode를 지정해줄 수 있습니다. Default모드는 `debug` 모드입니다. 만약 Default상태로 사용하고 싶은 경우에는, `config()`함수를 호출할 필요가 없습니다. 모드로는 `debug`, `production` 두가지 모드가 있습니다. 

3. `Method`에 데코레이터 적용해 보기
`Method`에서 Validator를 적용하기 위해서는 위와 동일하게, `staticCheck` 옵션도 사용할 수 있습니다. 다만, 제약사항으로 `Method`에서는 `isTypeMethod=True` 옵션을 **필수적으로 입력**해 주어야 합니다. 해당 불편 사항은 앞으로 추가될 `@HintBaseValidator`과 `@ParameterValidator`의 업데이트를 통해 개선해 나갈 예정입니다.

- Sequence type + strictCheck=False
```python

#Console
#Success to validate parameter types of function 'example_method'
#10 hello Name : hoplin

class Person(object):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Name : {self.name}"

class example_class(object):

    @parameter_validator(int,str,Person,isTypeMethod=True)
    def example_method(self,a,b,c):
        print(a,b,c)

ec = example_class()
ec.example_method(10,'hello',Person('hoplin'))
```

- Sequence type + strictCheck=False

```python

#Console
#Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function 'example_method' - Not nullable : 3 / Not checked counter : 1
#10 hello Name : hoplin

class Person(object):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Name : {self.name}"

class example_class(object):

    @parameter_validator(int,str,strictCheck=False,isTypeMethod=True)
    def example_method(self,a,b,c):
        print(a,b,c)

ec = example_class()
ec.example_method(10,'hello',Person('hoplin'))
```

- Key-Value type + strictCheck=True
```python
#Console
#Success to validate parameter types of function 'example_method'
#10 hello Name : hoplin
class Person(object):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Name : {self.name}"

class example_class(object):

    @parameter_validator(c=Person,a=int,b=str,isTypeMethod=True)
    def example_method(self,a,b,c):
        print(a,b,c)

ec = example_class()
ec.example_method(10,'hello',Person('hoplin'))
```
- Key-Value type + strictCheck=False
```python
#Console
#Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function 'example_method' - Not nullable : 2 / Not checked counter : 1
#10 Name : hoplin 50

class Person(object):
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return f"Name : {self.name}"

class example_class(object):

    @parameter_validator(b=Person,strictCheck=False,isTypeMethod=True)
    def example_method(self,a,b,c=30):
        print(a,b,c)

ec = example_class()
ec.example_method(10,Person('hoplin'),50)
```
***

## Test Case Result

![image](https://user-images.githubusercontent.com/45956041/198455932-3df0e1d5-2002-45a0-82d4-5490e7718449.png)
