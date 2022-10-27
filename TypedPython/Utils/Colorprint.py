class Colors:
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    RESET = '\033[0m'

    @classmethod
    def warning(cls,msg):
        return f"{Colors.BRIGHT_YELLOW}{msg}{Colors.RESET}"

    @classmethod
    def success(cls,msg):
        return f"{Colors.BRIGHT_GREEN}{msg}{Colors.RESET}"

