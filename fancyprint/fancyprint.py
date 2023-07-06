import sys
from contextlib import redirect_stdout
from .misc import Symbols, MessageType, TerminalColors, MessageFilter
from typing import Optional

class FancyPrintContext:
    
    def __init__(self, message: Optional[str] = None, msgtype: Optional[MessageType] = None) -> None:
        self.msgtype = msgtype
        self.open = False
        if msgtype is not None:
            self.new_chunk(message, msgtype)
            
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.end_chunk()
            
    def new_chunk(self, message: str, msgtype: MessageType) -> None:
        if msgtype in MESSAGE_FILTER:
            return 
        if self.open and not settings["autoclose_chunks"]:
            raise Exception("Chunk already open")
        elif self.open and settings["autoclose_chunks"]:
            self.end_chunk()
        
        self.msgtype = msgtype
        header = colorize(f"{Symbols.MULTI_LINE_CHUNK_START} {msgtype.ljust(5)}", msgtype_to_terminal_color[msgtype])
        _fprint(f"{header} {message}", msgtype)
        self.open = True
        
    def end_chunk(self) -> None:
        if self.open:
            print(colorize(Symbols.MULTI_LINE_CHUNK_END, msgtype_to_terminal_color[self.msgtype]))
            print('\n')
        self.msgtype = None
        self.open = False
        
    def print(self, message: str, msgtype : Optional[MessageType] = None) -> None:
        if not self.open:
            if msgtype is None:
                raise Exception("No chunk found to attach message to. Please specify a message type")
            else:
                self.print_single(message, MessageType)
                return
        header_symb = colorize(Symbols.MULTI_LINE_CHUNK_CONTD, msgtype_to_terminal_color[self.msgtype])
        if msgtype is not None:
            header_text = colorize(msgtype.ljust(5), msgtype_to_terminal_color[msgtype])
        else:
            header_text = colorize(MessageType.VOID.ljust(5), msgtype_to_terminal_color[self.msgtype])
        header = f"{header_symb} {header_text}"
        _fprint(f"{header} {message}", msgtype or self.msgtype)
        
    def print_single(self, message: str, msgtype: MessageType) -> None:
        if self.open and settings["autoclose_chunks"]:
            self.end_chunk()
        elif self.open and not settings["autoclose_chunks"]:
            raise Exception("Chunk already open")
        header = colorize(f"{Symbols.SINGLE_LINE_CHUNK} {msgtype.ljust(5)}", msgtype_to_terminal_color[msgtype])
        _fprint(f"{header} {message}", msgtype)
        
class Fancyfier:
    
    def __init__(self, stdout):
        self.buffer = []
        self.default_stdout = stdout
        self.buffer_idx = 0
        
    def write(self, stuff):
        if stuff == "\n":
            with redirect_stdout(self.default_stdout):
                GLOBAL_CONTEXT.print("".join(self.buffer[self.buffer_idx:]))
            self.buffer_idx = len(self.buffer)
            
        else:
            self.buffer.append(stuff)
    
def fancyfy(fn):
    def wrapper(*args, **kwargs):
        old_stdout = sys.stdout
        f = Fancyfier(old_stdout)
        with redirect_stdout(f):
            fn(*args, **kwargs)
    return wrapper

def _fprint(message : str, message_type : Optional[MessageType] = None):
    if message_type in MESSAGE_FILTER:
        return
    print(message, flush=settings["autoflush"])

def colorize(msg, color : TerminalColors):
    if settings["nocolor"]:
        return msg
    return f"{color}{msg}{TerminalColors.ENDC}"

def info(message : str):
    GLOBAL_CONTEXT.print_single(message, MessageType.INFO)
    
def ok(message : str):
    GLOBAL_CONTEXT.print_single(message, MessageType.OK)
    
def error(message : str):
    GLOBAL_CONTEXT.print_single(message, MessageType.ERROR)
    
def debug(message : str):
    GLOBAL_CONTEXT.print_single(message, MessageType.DEBUG)
    
def warning(message : str):
    GLOBAL_CONTEXT.print_single(message, MessageType.WARNING)
    
def print_enum(dictionary : dict, 
               message_type: Optional[MessageType] = None, 
               message: Optional[str] = "", 
               max_key_len: Optional[int] = None, 
               max_val_len: Optional[int] = None, 
               keep_open: Optional[bool]=False):
    if not GLOBAL_CONTEXT.open:
        if message_type is None:
            raise Exception("No chunk found to attach enumeration to. Please specify a message type")
        else:
            GLOBAL_CONTEXT.new_chunk(message, message_type)
    keys = dictionary.keys()
    max_key_ljust = max_key_len or max([len(key) for key in keys])
    max_val_ljust = max_val_len
    for key, val in dictionary.items():
        GLOBAL_CONTEXT.print(f"{Symbols.ENUMERATION} {key.ljust(max_key_ljust)[:max_key_len]} = {str(val)[:max_val_ljust]}")
    if not keep_open:
        GLOBAL_CONTEXT.end_chunk()

settings = {
    "autoflush" : False, # whether to flush after every print. Use this when redirecting output to a file
    "autoclose_chunks" : True, # whether to autoclose chunks when a new chunk is opened. If False, an exception will be raised.
    "nocolor": False # whether to disable colorized output
}

msgtype_to_terminal_color = {
    MessageType.INFO: TerminalColors.OKBLUE,
    MessageType.OK: TerminalColors.OKGREEN,
    MessageType.ERROR: TerminalColors.FAIL,
    MessageType.DEBUG: TerminalColors.OKCYAN,
    MessageType.WARNING: TerminalColors.WARNING
}

# Initialise fancyprint on import
GLOBAL_CONTEXT = FancyPrintContext()
MESSAGE_FILTER = MessageFilter([])