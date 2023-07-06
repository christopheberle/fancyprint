class Symbols:
    MULTI_LINE_CHUNK_START = "⎡"
    MULTI_LINE_CHUNK_CONTD = "⎢"
    MULTI_LINE_CHUNK_END = "⎣"
    SINGLE_LINE_CHUNK = "["
    ENUMERATION = "•"

class MessageType:
    INFO = "INFO"
    OK = "OKAY"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    WARNING = "WARN"
    VOID = ""
    
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class MessageFilter(set):
    
    def __setitem__(self, index: int, value: MessageType):
        if isinstance(value, MessageType):
            super().__setitem__(index, value)
        else:
            raise TypeError("Filter must be of type MessageType")
        
    def add(self, __object) -> None:
        if isinstance(__object, MessageType):
            super().add(__object)
        else:
            raise TypeError("Filter must be of type MessageType")
        
    def discard(self, __object) -> None:
        if isinstance(__object, MessageType):
            super().discard(__object)
        else:
            raise TypeError("Filter must be of type MessageType")