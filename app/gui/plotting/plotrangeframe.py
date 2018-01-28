from tkinter import *

from app.gui.dialog.footnote_text import FootnoteDialog
from app.gui.plotting import BBOX
from app.gui.plotting.drag_handler import DragHandler
from app.gui.plotting.plot_canvas import PlotCanvas

from matplotlib.figure import Figure
import matplotlib.text
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

class PlotRangeFrame(Frame):
    def __init__(self, parent, title="RSG", annotation_id=None):
        super().__init__(parent)
        self.canvas = PlotCanvas(Figure((10, 6), dpi=100), self)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.title = title
        self.sample = None
        self._handler = DragHandler(self.canvas, self.set_label_pos)
        self._fnid = annotation_id
        self._footnote = matplotlib.text.Text(0.0, 0.0, "", bbox=BBOX, wrap=True)
        self._footnote_frame = Frame(self)
        self._has_footnote = False
        self._fn_add_button = Button(self._footnote_frame, text="Add Footnote", command=self._footnote_addrem_click)
        self._fn_mod_button = Button(self._footnote_frame, text="Footnote Text", command=self._footnote_text_click, state=DISABLED)
        self.build()

    def _footnote_addrem_click(self):
        if not self._has_footnote:
            res = FootnoteDialog(self, "").run()
            if not res['cancelled']:
                self._set_footnote(text=res['text'])
        else:
            self._remove_footnote()
        self.canvas.draw()

    def _footnote_text_click(self):
        res = FootnoteDialog(self, self.sample.labels[self._fnid]['text']).run()
        if not res['cancelled']:
            self._set_footnote(text=res['text'])
        self.canvas.draw()

    def _set_footnote(self, pos=None, text=None):
        if not self._has_footnote:
            self._add_footnote()
        if pos is not None:
            self._footnote.set_position(pos)
            self.sample.labels[self._fnid].update(pos=pos)
        if text is not None:
            self._footnote.set_text(footnote_format(text))
            self.sample.labels[self._fnid].update(text=text)

    def _add_footnote(self):
        if self._has_footnote:
            return
        self.canvas.axes.add_artist(self._footnote)
        self.sample.labels[self._fnid] = {"text":"asdf", "pos":(1.0,1000.0)}
        self._footnote.set_position((1.0,1000.0))
        self._footnote.set_text("asdf")
        self._has_footnote = True
        self._handler.watch_label(self._fnid, self._footnote)
        self.button_set()

    def _remove_footnote(self):
        if not self._has_footnote:
            return
        self._footnote.remove()
        self._has_footnote = False
        del self.sample.labels[self._fnid]
        self._handler.ignore_label(self._fnid)
        self.button_set()

    def set_sample(self, sample):
        self.sample = sample
        title = sample.titles[0]
        t = 1
        while t != 3 and sample.titles[t] is not None and sample.titles[t] != "":
            title += "\n" + sample.titles[t]
            t += 1
        if title is None:
            title = ""
        title += "\n"+self.title+" (Sample {})".format(sample.num)
        self.canvas.set_labels(title=title)

        if self._fnid in sample.labels:
            info = sample.labels[self._fnid]
            self._set_footnote(info['pos'], info['text'])
        else:
            self._remove_footnote()

        self.canvas.show()

    def set_label_pos(self, label_id, label):
        self.sample.labels[label_id]['pos'] = label.get_position()

    def button_set(self):
        if self._has_footnote:
            self._fn_add_button['text'] = "Remove Footnote"
            self._fn_mod_button['state'] = NORMAL
        else:
            self._fn_add_button['text'] = "Add Footnote"
            self._fn_mod_button['state'] = DISABLED

    def build(self):
        self.canvas.pack()
        self._fn_add_button.pack(side=LEFT)
        self._fn_mod_button.pack(side=LEFT)
        self._footnote_frame.pack()

CHAR_PER_LINE = 20

def footnote_format(text):
    words = text.split(" ")
    line = ""
    ret = ""
    i = 0
    while i < len(words):
        while i < len(words) and len(line) + len(words[i]) <= CHAR_PER_LINE:
            line += " " + words[i]
            i += 1
        ret += line.strip() + "\n"
        line = ""
    return ret.strip()