IDLEAnalyzer
============

IDLE is an integrated development environment for Python, which has been bundled with each release of the language,
completely  written in Python and with the Tkinter GUI toolkit. In Python universe, there are  several metrics and 
defect capturing tools which assists developers on code quality improvement by enforcing adherence to coding best 
practices. IDLE Analyzer project is aimed to integrate these tools into IDLE editor as extensions of graphical tools 
which can be used on-the-fly.  

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

