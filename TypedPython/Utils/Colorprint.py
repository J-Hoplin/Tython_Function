from colorama import Fore,Style

'''
2022 / 11 / 01
Color print via unicode -> colorama
'''

class printer:
    @classmethod
    def fail(cls,msg):
        return f"{Fore.RED + Style.BRIGHT + msg}"

    @classmethod
    def warning(cls,msg):
        return f"{Fore.YELLOW + Style.BRIGHT + msg}"

    @classmethod
    def success(cls,msg):
        return f"{Fore.GREEN + Style.BRIGHT + msg}"

