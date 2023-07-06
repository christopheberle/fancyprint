from typing import List, Optional, Iterable, Any
from .fancyprint import FancyPrintContext
from .utils import stralign, TrackerFunctions
from collections import deque

class FancyTable:
    
    def __init__(self, 
                 colnames: List[str], 
                 colsizes: Optional[List[int]] = None, 
                 sep: Optional[str] = "|", 
                 align: Optional[str] = "l", 
                 idx: Optional[bool] = False, 
                 header: Optional[bool] = True, 
                 footer: Optional[bool] = True,
                 fpcontext: Optional[FancyPrintContext] = None):
        self.colnames = colnames
        self.align = align if isinstance(align, list) else [align for _ in range(len(colnames))]
        self.idx = idx
        if isinstance(colsizes, Iterable):
            self.colsizes = [max(len(cname), csize) for cname, csize in zip(self.colnames, colsizes)]
        elif isinstance(colsizes, int) or colsizes is None:
            self.colsizes = [max(len(cname), colsizes or 1) for cname in self.colnames]
        else:
            raise ValueError(f"Invalid colsizes {colsizes}")
        if self.idx:
            self.colnames = ["idx"] + self.colnames
            self.colsizes = [len("idx")] + self.colsizes
            self.align = ["r"] + self.align
        self.current_idx = 0
        self.colidxs = {c:i for i,c in enumerate(self.colnames)}
        self.sep = f" {sep.strip()} "
        self.header_str = self.sep.join([stralign(c, s, "c") for c,s in zip(self.colnames, self.colsizes)])
        self.tablewidth = len(self.header_str)
        self.needs_header = header
        self.needs_footer = footer
        self.print_fn = fpcontext.print if fpcontext is not None else print

    def __enter__(self):
        if self.needs_header:
            self.print_header()
            self.needs_header = False # avoid printing header again
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.needs_footer:
            self.print_footer()
            self.needs_footer = False # avoid printing footer again
    
    def print_footer(self):
        self.print_fn(len(self.header_str)*"-")
    
    def print_header(self):
        self.print_fn(self.header_str)
        self.print_fn(len(self.header_str)*"=")
    
    def print_row(self, *args):
        if self.needs_header:
            # if not used in context, print header
            self.print_header() 
            self.needs_header = False # avoid printing header again
        vals = list(args)
        if self.idx: 
            vals = [self.current_idx] + vals
        self.print_fn(self.sep.join([stralign(str(v), self.colsizes[self.colidxs[c]], self.align[self.colidxs[c]])[:self.colsizes[self.colidxs[c]]] for c,v in zip(self.colnames, vals)]))
        self.current_idx += 1
        
    def print(self, *args, **kwargs):
        if all([isinstance(a, Iterable) for a in args]):
            vals = zip(*args)
        else:
            vals = zip(*[[a] for a in args])
        for tup in vals:
            self.print_row(*tup, **kwargs)
        
        
class FancyChangeTracker:
    
    AVAIL_QUANTITIES = [fn_name for fn_name in dir(TrackerFunctions) if not fn_name.startswith("__")]
    
    def __init__(self, var_name: str, quantities: Optional[str | List[str]] = "delta", max_history: Optional[int] = None, **formatting_kwargs):
        if isinstance(quantities, str):
            quantities = [quantities]
        assert all([q in self.AVAIL_QUANTITIES for q in quantities])
        self.var_name = var_name
        self.var_hist = deque([], maxlen=max_history) if max_history is not None else []
        
        self.fn_dir = {fn_name: getattr(TrackerFunctions, fn_name) for fn_name in quantities}
        self.table = FancyTable([var_name] + quantities, **formatting_kwargs)
        
    def update(self, var: Any):
        self.var_hist.append(var)
        fn_vals = [fn(self.var_hist) for fn in self.fn_dir.values()]
        self.table.print_row(var, *fn_vals)