from tkinter import Button

from app.gui.frame.abstract_tab_frame import AbstractTabFrame
from app.gui import GUI_FONT
from app.gui.input_group.sample_file_input import SampleFileInputGroup
from app.gui.input_group.sample_name_input import SampleNameInputGroup


class ASCDataFrame(AbstractTabFrame):
    """Get sample # and data file"""

    def __init__(self, parent, proj_ptr, next_frame):
        super().__init__(parent, "Raw Data", proj_ptr, next_frame)
        self.name_input = SampleNameInputGroup(self, font=GUI_FONT)
        self.dir_input = SampleFileInputGroup(self, font=GUI_FONT)
        self.name_input.pack(pady=15)
        self.dir_input.pack(pady=15)
        Button(self, font=GUI_FONT, text="Done", command=self.on_next).pack()

    def content_update(self):
        s = self._proj_handle.curr_sample

        # Create a "suggested name" based on current number of samples in the project.
        if s.name is not None:
            self.name_input.set(s.name)
        else:
            n_samples = self._proj_handle.project.num_samples()
            self.name_input.set(f"Sample {n_samples}")

        if s.dir is None:
            self.dir_input.set_dir("")
        else:
            self.dir_input.set_dir(s.dir)
        self.dir_input.set_initialdir(self._proj_handle.project.data_dir)

    def is_done(self):
        return self.name_input.entries_valid() and self.dir_input.entries_valid()

    def unload(self):
        s = self._proj_handle.curr_sample
        s.name = self.name_input.get_value()
        s.set_data_from_file(self.dir_input.get_dir())
