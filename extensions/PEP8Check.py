"""PEP8Check- Extension to call the PEP8 code checker to check style

It is nice to have a reminder that the Python code style conforms to PEP 8
the official Python style guide.  Need to add a better comment up here.

"""
import tkinter
from tkinter.constants import (TOP, LEFT, RIGHT, X, Y, W, E, N, S, NW, SUNKEN,
                               RAISED, BOTTOM, RIDGE, HORIZONTAL, END, NE)
import re
from sys import maxsize as INFINITY
from idlelib.configHandler import idleConf
import pep8
import io
import sys


UPDATEINTERVAL = 1000  # millisec
FONTUPDATEINTERVAL = 1000  # millisec


class PEP8Check:  # this is the IDLE extension code
    menudefs = [('options', [('!PEP8 Check', '<<toggle-pep8check>>')])]

    bgcolor = idleConf.GetOption("extensions", "PEP8Check",
                                 "bgcolor", type="str", default="LightGray")
    fgcolor = idleConf.GetOption("extensions", "PEP8Check",
                                 "fgcolor", type="str", default="Black")

    def __init__(self, editwin):

        self.counter = 0
        self.editwin = editwin
        self.text = editwin.text
        self.textfont = self.text["font"]
        self.verticalLabelFrame = None
        self.pep8_output = ""
        # pep8_output_frames is an array contains error/warning messages, 
        # error codes as buttons, line:col numbers and a resolve button
        # A set of above itmes are generated dynamically with pep8 output
        self.pep8_output_frames = []
        self.highlightedline = None
        self.highlightedcol = None
        self.prei = None
        # self.info is a list of (line number, indent level, line text, block
        # keyword) tuples providing the block structure associated with
        # self.topvisible (the linenumber of the line displayed at the top of
        # the edit window). self.info[0] is initialized as a 'dummy' line which
        # starts the toplevel 'block' of the module.
        self.info = [(0, -1, "", False)]
        self.topvisible = 1
        visible = idleConf.GetOption("extensions", "PEP8Check",
                                     "visible", type="bool", default=False)
        if visible:
            self.toggle_pep8check_event()
            
    def toggle_pep8check_event(self, event=None):
        if not self.verticalLabelFrame:
            # Calculate the border width and horizontal padding required to
            # align the context with the text in the main Text widget.
            #
            # All values are passed through int(str(<value>)), since some
            # values may be pixel objects, which can't simply be added to ints.
            widgets = self.editwin.text, self.editwin.text_frame
            # Calculate the required vertical padding
            padx = 0
            pady = 0
            for widget in widgets:
                padx += int(str( widget.pack_info()['padx'] ))
                padx += int(str( widget.cget('padx') ))
                pady += int(str(widget.pack_info()['pady']))
                pady += int(str(widget.cget('pady')))
            # Calculate the required border width
            border = 0
            for widget in widgets:
                border += int(str(widget.cget('border')))

            self.topLabel = tkinter.Label(self.editwin.top,
                                       text="PEP8 Style Check Mode",
                                       anchor=W, justify=LEFT,
                                       font=self.textfont,
                                       bg=self.bgcolor, fg=self.fgcolor,
                                       width=1, #don't request more than we get
                                       padx=padx, border=border,
                                       relief=SUNKEN)

            self.verticalLabelFrame = tkinter.LabelFrame(self.editwin.top,
                                                         text=
                                                         "PEP8 Style Check",
                                                         bg=self.bgcolor,
                                                         fg=self.fgcolor,
                                                         width=pady,
                                                         border=border,
                                                         relief=SUNKEN)
            self.configButton = tkinter.Button(self.topLabel,
                                          text="Configure PEP8",
                                          command=self.update)
            self.closePep8Button = tkinter.Button(self.topLabel,
                                          text="Exit PEP8 mode",
                                              command = self.toggle_pep8check_event)
            
            #configure pep8 controls
            

            #packing all pep8 windows and controls
            self.topLabel.pack(side=TOP, fill=X, expand=False,
                            before=self.editwin.text_frame)
            self.verticalLabelFrame.pack(side=RIGHT, fill=Y, expand=True)
            self.closePep8Button.pack(side=RIGHT)
            self.configButton.pack(side=RIGHT)  
            #self.editwin.top = tkinter.Tk()
            #var = tkinter.IntVar()
            #self.c = tkinter.Checkbutton(self.topLabel, text="Expand", variable=var, onvalue = 1, offvalue = 0)

            #self.c.pack(after=self.editwin.top)
 
            self.editwin.setvar('<<toggle-pep8check>>', True)         
            self.update()
        else:
            self.verticalLabelFrame.destroy()
            self.verticalLabelFrame = None
            self.configButton.destroy()
            self.configButton = None
            self.closePep8Button.destroy()
            self.closePep8Button = None
            self.topLabel.destroy()
            self.topLabel = None
            self.editwin.setvar('<<toggle-pep8check>>', False) 


        idleConf.SetOption("extensions", "PEP8Check", "visible",
                           str(self.verticalLabelFrame is not None))
        idleConf.SaveUserCfgFiles()

    def update(self):
        """Update context information and lines visible in the context pane.

        """
        if self.highlightedline is not None:
            self.remove_highlight(self.highlightedline, self.highlightedcol)

        self.run_pep8()
        for items in self.pep8_output_frames:
            items[0].pack_forget()
        del self.pep8_output_frames[:]

        maxMessages = 15
        i = 0
        for line in iter(self.pep8_output.splitlines()):

            if(i < maxMessages):
                details = line.split(":")
                lineno = details[1]
                colno = details[2]
                code = details[3][1:6]
                message = details[3][6:]
                if(code.startswith("E")):
                    error = True
                    codecolor = "red"
                else:
                    error = False
                    codecolor = "#FFBF00"

                messageLabelFrame = tkinter.LabelFrame(self.verticalLabelFrame)
                codeButton = tkinter.Button(messageLabelFrame, text=code,
                                            bg=codecolor,
                                            width=5,
                                            command=lambda j=lineno,
                                            k=colno, l=i:
                                            self.highlight(j, k, l))
                lineColLabel = tkinter.Label(messageLabelFrame,
                                             text=lineno+":"+colno)
                messageLabel = tkinter.Label(messageLabelFrame, text=message)
                resolveButton = tkinter.Button(messageLabelFrame,
                                               text="Resolved",
                                               bg="#03CF47",
                                               command=self.update)

                messageLabelFrame.pack(side=TOP, fill=X, expand=False)
                codeButton.pack(side=LEFT)
                lineColLabel.pack(side=LEFT)
                messageLabel.pack(side=LEFT)

                items = []
                items.append(messageLabelFrame)
                items.append(codeButton)
                items.append(lineColLabel)
                items.append(messageLabel)
                items.append(resolveButton)
                self.pep8_output_frames.append(items)

                i += 1
            else:
                break

    def highlight(self, lineno, colno, i):

        self.remove_highlight(self.highlightedline, self.highlightedcol)

        if self.prei is not None:
            self.pep8_output_frames[self.prei][4].pack_forget()
            self.pep8_output_frames[self.prei][3].configure(bg=self.bgcolor)
        self.prei = i

        self.pep8_output_frames[i][4].pack(side=BOTTOM)
        self.pep8_output_frames[i][3].configure(bg="#E4143D")

        #TODO Find line number is lacking by one line form run_pep8
        lineno = int(lineno)-1

        #highlight the line
        self.text.tag_add(str(lineno), str(lineno)+".0", str(lineno)+".end")
        self.text.tag_config(str(lineno), background="yellow",
                             foreground="blue")
        #highlight the indicated char with one before and after.
        self.text.tag_add(str(colno), str(lineno)+"."+str(colno)+"-1c",
                          str(lineno)+"."+str(colno))
        self.text.tag_config(str(colno), background="red", foreground="blue")

        #auto schroll editorwindow to 10 lines before requested line
        self.text.yview(str(lineno)+".0-10lines")
        self.highlightedline = lineno
        self.highlightedcol = colno

    def remove_highlight(self, lineno, colno):
        if self.highlightedline is not None:
            #remove the presious highlights
            self.text.tag_remove(str(lineno), str(lineno)+".0-2lines",
                                 str(lineno)+".end+2lines")
            self.text.tag_remove(str(colno), str(lineno)+".0-2lines",
                                 str(lineno)+".0+2lines")

    def run_pep8(self):
        # redirect standard output to a StringIO, this is done because PEP8
        # prints results to standard output.  This is a much better hack then
        # modifying pep8
        old_stdout = sys.stdout
        captured_stdout = io.StringIO()
        sys.stdout = captured_stdout
        lastLine = int(self.text.index('end-1c').split('.')[0])
        codeLines = []
        for i in range(0, lastLine):
            # pep8 needs eol
            text = self.text.get("%d.0" % i, "%d.end" % i) + "\n"
            codeLines.append(text)

        pep8IDLE = pep8.Checker(filename=None, lines=codeLines)
        results = pep8IDLE.check_all()
        self.pep8_output = captured_stdout.getvalue()
        sys.stdout = old_stdout
