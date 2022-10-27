from TypedPython.Utils.Colorprint import Colors

class MSGS:

    @classmethod
    def warning_nonsafe(cls,functionname,required_field,checking_field):
        print(Colors.warning(f"Potential warning : Some arguments are not-nullable but not enrolled in validator's decorator of function '{functionname}' - Not nullable : {required_field} / Not checked counter : {checking_field}"))

    @classmethod
    def success_successmsg(cls,functionname):
        print(Colors.success(f"Success to validate parameter types of function '{functionname}'"))