from tkinter import Frame, Menu, filedialog, Tk, RIGHT, BOTH
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class App (Frame):
    GRAPH_SPACE_RATIO = 0.1
    def __init__ (self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.build()
    def build(self):
        self.parent.title ("RSGrapher")
    		
         # Create Menubar container and give it to root
        menubar = Menu (self.parent)
        self.parent.config (menu=menubar)
        
        filemenu = Menu (menubar)
        filemenu.add_command (label="Open", command=self.openfile)
        filemenu.add_command (label="Export Graphs", command=self.noimp)
        filemenu.add_separator()
        filemenu.add_command (label="Quit", command=self.quit)
        menubar.add_cascade (label="File", menu=filemenu)
        		
        f = Figure (figsize=(5,5), dpi=100)
        p = f.add_subplot (111)
        self.stresscurve, = p.plot ([x for x in range(100)],[y**2 for y in range(100)])
        
        self.canvas = FigureCanvasTkAgg (f, master=self.parent)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH,expand=True)
        		
    def noimp (self):
        print ("This function is not implemented.")
        	
    def openfile (self):
        fh = open(filedialog.askopenfilename(title = "Open ASC File"))
        x=[]
        y=[]
        for i in range(7):
            fh.readline()
        line = fh.readline().strip()
        while (line != ""):
            t, d, l = line.split ("\t",2)
            x.append (float(d))
            y.append (float(l))
            line = fh.readline().strip()
        xm = max(x)
        ym = max(y)
        		
        fh.close()
        self.stresscurve.set_xdata (x)
        self.stresscurve.set_ydata (y)
        self.stresscurve.axes.set_xbound(0, xm+App.GRAPH_SPACE_RATIO*xm)
        self.stresscurve.axes.set_ybound(0, ym+App.GRAPH_SPACE_RATIO*ym)
        self.canvas.show()

#---------------------------------------------------------------

#		Main Loop
print ("Running")
root = Tk()
print ("Tk object created")
app = App(root)
print ("Created App")
root.mainloop()
