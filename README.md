IDLEAnalyzer
============

IDLE is an integrated development environment for Python, which has been bundled with each release of the language,
completely  written in Python and with the Tkinter GUI toolkit. In Python universe, there are  several metrics and 
defect capturing tools which assists developers on code quality improvement by enforcing adherence to coding best 
practices. IDLE Analyzer project is aimed to integrate these tools into IDLE editor as extensions of graphical tools 
which can be used on-the-fly.  

#### Features 


1. Style defect dapturing using pep8 tool
  On-the-fly syntax checking and highlighting of PEP8 python style conventions.

 (TODOs)
2. Metrics details using Pymetrix.
   Reporting of code meassures including McCabe's Cyclomatic Complexity metric, LoC and %Comments.

3. Passive checking of code using PyFlakes. 
  On-the-fly syntax highlighting and error checking.


#### Installation


- Append all contents of config-extensions.cfg to <YourPythonDirectory>/idlelib/config-extensions.cfg
     (On my ubuntu <YourPythonDirectory> means /usr/lib/python2.7)
    
- Copy extensions/PEP8Check.py and analyzers/pep8.py into <YourPythonDirectory>/idlelib
      This requires root access (sudo), So I did followings,
        ```sudo su```
        ```cp -r extensions/PEP8Check.py /usr/lib/python2.7/idlelib```
        ```cp -r analyzers/pep8.py /usr/lib/python2.7/idlelib```

#### Usage

1. Style Defects with Pep8.
    * After this installation IDLE will show PEP8 style check toggle menu in Options.
    * Once PEP8 check enabled the current module is checked by pep8 tool and the defects will be shown in a extended left pane. 
    *Defect codes will be listed as a Buttons, button click leads to highlighting the line and column of the defect and scroll editor window if needed. 
    *It is expected that the developer will correct the defect with the help of the message and eventually press the Resolved button,which refresh the pane.

2. Metrics details.
    TODO

3. PyFlakes Check
    TODO //


#### On Python Issue Tracker

This is a project initiated as "IDLE: PEP8 Style Check Integration" in python issue tracker at http://bugs.python.org/issue18704 
The initial work is submmited as a CPython patch and the idea is getting more generalized with core Python developers suggestions on that issue.
This developement extends the works done with the patch, named as IDLE Analyzer to enable the usefull features to Python developers.



