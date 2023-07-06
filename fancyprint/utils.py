from typing import Iterable
import numpy as np

def stralign(s : str, length: int, mode : str) -> str:
    match mode:
        case "l":
            return s.ljust(length)
        case "r":
            return s.rjust(length)
        case "c":
            return s.center(length)
        case _:
            raise ValueError(f"Invalid align mode {mode}")
        
def sgnnum(n : float):
    return f"{n:+}"

class TrackerFunctions:
    
    @staticmethod
    def delta(hist: Iterable[float]):
        if len(hist) < 2:
            return np.nan
        return hist[-1]-hist[-2]
    
    @staticmethod
    def absdelta(hist: Iterable[float]):
        if len(hist) < 2:
            return np.nan
        return abs(hist[-1]-hist[-2])
    
    @staticmethod
    def reldelta(hist: Iterable[float]):
        if len(hist) < 2:
            return np.nan
        return (hist[-1]-hist[-2])/hist[-2]
    
    @staticmethod
    def absreldelta(hist: Iterable[float]):
        if len(hist) < 2:
            return np.nan
        return abs((hist[-1]-hist[-2])/hist[-2])
    
    @staticmethod
    def mean(hist: Iterable[float]):
        return np.mean(hist)
    
    @staticmethod
    def std(hist: Iterable[float]):
        return np.std(hist)
    
    @staticmethod
    def var(hist: Iterable[float]):
        return np.var(hist)