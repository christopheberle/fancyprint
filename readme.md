# FancyPrint

Working on high-performance clusters is ugly but it doesn't have to be! FancyPrint is a small package containing helpers to make terminal outputs just a little more fancy 💅.

## Getting Started

### FancyPrintContexts

A `FancyPrintContext` is the central part of FancyPrint. It manages the grouping of several print statements into groups called chunks. Each such chunk is associated with a certain type of information the group of print statements conveys. The following types are available

* `MessageType.INFO`
* `MessageType.OK`
* `MessageType.DEBUG`
* `MessageType.ERROR`
* `MessageType.WARNING`


```python
import fancyprint as fp

with fp.FancyPrintContext("Here is some info", fp.MessageType.INFO) as fpc:
    fpc.print("Here is some more info")

with fp.FancyPrintContext("All ok", fp.MessageType.OK) as fpc:
    fpc.print("Very nice :)")
    
with fp.FancyPrintContext("Here is some debug info", fp.MessageType.DEBUG) as fpc:
    fpc.print("Here is some more debug info")
    
with fp.FancyPrintContext("Oh no an error", fp.MessageType.ERROR) as fpc:
    fpc.print("Explain what went wrong here")
    
with fp.FancyPrintContext("Oops a warning", fp.MessageType.WARNING) as fpc:
    fpc.print("Explain what went wrong here")
```

    [94m⎡ INFO [0m Here is some info
    [94m⎢[0m [94m     [0m Here is some more info
    [94m⎣[0m
    [92m⎡ OKAY [0m All ok
    [92m⎢[0m [92m     [0m Very nice :)
    [92m⎣[0m
    [96m⎡ DEBUG[0m Here is some debug info
    [96m⎢[0m [96m     [0m Here is some more debug info
    [96m⎣[0m
    [91m⎡ ERROR[0m Oh no an error
    [91m⎢[0m [91m     [0m Explain what went wrong here
    [91m⎣[0m
    [93m⎡ WARN [0m Oops a warning
    [93m⎢[0m [93m     [0m Explain what went wrong here
    [93m⎣[0m


Sometimes we just need to print a single-line status update. In this case we can use the `print_single` method as follows:


```python
fpc.print_single("This is a single-line warning", fp.MessageType.WARNING)
```

    [93m[ WARN [0m This is a single-line warning


For convenience FancyPrint defines the following aliases 
* `print_info`
* `print_ok`
* `print_error`
* `print_debug`
* `print_warning`

which eliminate the need to specify the message type.


```python
fp.print_warning("This is a single-line warning")
```

    [93m[ WARN [0m This is a single-line warning


# The global context

When imported FancyPrint sets up a `FancyPrintContext` for you automatically called `GLOBAL_CONTEXT`. To start a chunk right away you can do the following:


```python
fp.GLOBAL_CONTEXT.new_chunk("This is a chunk", fp.MessageType.INFO)
fp.GLOBAL_CONTEXT.end_chunk()
```

    [94m⎡ INFO [0m This is a chunk
    [94m⎣[0m
    
    


## Different Message Types within the same chunk

Sometimes we need to print messages with a different status than the encapsulating chunk without giving up the visual grouping. This can be done by providing a `MessageType` when printing within a chunk.


```python
with fp.FancyPrintContext("Here is some info", fp.MessageType.INFO) as fpc:
    fpc.print("Here is some more info")
    fpc.print("Here is some additional info when debugging", fp.MessageType.DEBUG)
    fpc.print("Even more info")
    fpc.print("A warning came up", fp.MessageType.WARNING)
```

    [94m⎡ INFO [0m Here is some info
    [94m⎢[0m [94m     [0m Here is some more info
    [94m⎢[0m [96mDEBUG[0m Here is some additional info when debugging
    [94m⎢[0m [94m     [0m Even more info
    [94m⎢[0m [93mWARN [0m A warning came up
    [94m⎣[0m
    
    


# Quality of life functions

FancyPrint contains a couple of functions to make life just a little easier.


```python
params = {"a" : 2, "b": 12.3213, "c" : "hello", "d" : True}
fp.print_enum(params, fp.MessageType.INFO, "Parameters")
```

    [94m⎡ INFO [0m Parameters
    [94m⎢[0m [94m     [0m • a = 2
    [94m⎢[0m [94m     [0m • b = 12.3213
    [94m⎢[0m [94m     [0m • c = hello
    [94m⎢[0m [94m     [0m • d = True
    [94m⎣[0m
    
    



```python
import numpy as np
from fancytables import FancyTable
epochs = np.arange(10)
loss = np.random.rand(10).cumsum()[::-1]
FancyTable(["epoch", "loss"], [5, 10]).print(epochs, loss)
```

    epoch |    loss   
    ==================
    0     | 5.84484686
    1     | 5.23525243
    2     | 4.89788282
    3     | 4.86022193
    4     | 4.15116868
    5     | 3.22414394
    6     | 2.31917861
    7     | 1.75547750
    8     | 0.89670580
    9     | 0.30191273



```python
from fancytables import FancyChangeTracker
tracker = FancyChangeTracker("loss", quantities=["absdelta", "absreldelta"], idx=True)
for epoch in epochs:
    tracker.update(loss[epoch])
```

    idx | loss | absdelta | absreldelta
    ===================================
      0 | 5.84 | nan      | nan        
      1 | 5.23 | 0.609594 | 0.104296049
      2 | 4.89 | 0.337369 | 0.064441899
      3 | 4.86 | 0.037660 | 0.007689217
      4 | 4.15 | 0.709053 | 0.145889068
      5 | 3.22 | 0.927024 | 0.223316566
      6 | 2.31 | 0.904965 | 0.280683911
      7 | 1.75 | 0.563701 | 0.243060668
      8 | 0.89 | 0.858771 | 0.489195502
      9 | 0.30 | 0.594793 | 0.663309048



```python

```
