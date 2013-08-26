IDLEAnalyzer
============

IDLE is an integrated development environment for Python, which has been bundled with each release of the language,
completely  written in Python and with the Tkinter GUI toolkit. In Python universe, there are  several metrics and 
defect capturing tools which assists developers on code quality improvement by enforcing adherence to coding best 
practices. IDLE Analyzer project is aimed to integrate these tools into IDLE editor as extensions of graphical tools 
which can be used on-the-fly.  

Features 
========

1. Style defect dapturing using pep8 tool
  On-the-fly syntax checking and highlighting of PEP8 python style conventions.

 (TODOs)
2. Metrics details using Pymetrix.
   Reporting of code meassures including McCabe's Cyclomatic Complexity metric, LoC and %Comments.

3. Passive checking of code using PyFlakes. 
  On-the-fly syntax highlighting and error checking.


Installation
============

- Install pep8 (In unix this is sudo apt-get install pep8 )

- Append config-extensions .cfg to ~/.idlerc/config-extensions.cfg
      (If it doesn't exist yet copy the file over)
    
- Copy StyleCheck.py and DocTest.py into idlelib/extensions
      which is found in the Python directory
      (On my Mac this is /System/Library/Frameworks/Python.framework/
                      Versions/2.7/lib/python2.7/idlelib)
      This requires root access (sudo). 

