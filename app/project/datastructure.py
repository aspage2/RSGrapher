import os

INI_FILE = "project.ini"

"""
    PROJECT FILE STRUCTURE

    project_name
    |  Excel Data
    |  Photos
    |  pdfs for Test Report
    |  Photos
    |  Samples
    |  |  sample_1_name
    |  |  |  sample.dat
    |  |  |  other stuff
    |  |  sample_2_name
    |  |  |  sample.dat
    |  |  |  other stuff
    |  Stress Strain Data
    |  project.ini
"""


def create_project(directory, project_title, project_num, project_desc):
    file_location = directory + "/" + proj_folder_name(project_title, project_num)
    os.mkdir(file_location)
    os.mkdir(file_location + "/Samples")
    os.mkdir(file_location + "/Photos")
    os.mkdir(file_location + "/pdfs for Test Report")
    os.mkdir(file_location + "/Excel Data")
    os.mkdir(file_location + "/Stress Strain Data")
    meta_file = open(file_location + "/project.ini", "w+")
    meta_file.write("RSG " + str(project_num) + "\n")
    meta_file.write(project_title + "\n")
    meta_file.write(project_desc + "\n")
    meta_file.close()


def proj_folder_name(project_title, project_num):
    return "RSG" + str(project_num) + " - " + project_title


class Project:
    """A handler for projects."""

    def __init__(self, project_dir=None):
        if project_dir is not None:
            self.open(project_dir)
        else:
            self.empty_project()

    def add_sample(self, ascdata, name, diameter):
        """Add a sample to this project"""
        self.fail_on_closed()
        sample_dir = self.dir + "/Samples/" + name
        os.mkdir(sample_dir)
        data = open(sample_dir + "/sample.dat", "w+")
        data.write(name + "\n")
        data.write(str(diameter) + "\n")
        for i in range(len(ascdata)):
            disp, load = ascdata[i]
            data.write(str(disp) + "\t" + str(load) + "\n")
        data.close()
        project_meta = open(self.dir + "/" + INI_FILE, "a")
        project_meta.write("SAMPLE\t" + name + "\n")
        project_meta.close()
        self.samples.append(Sample(sample_dir))
        self.set_sample(name)

    def set_sample(self, name):
        for s in self.samples:
            if s.name == name:
                self.curr_sample = s

    def empty_project(self):
        """Empty this project"""
        self.dir = None
        self.num = ""
        self.title = ""
        self.desc = ""
        self.samples = []
        self.curr_sample = None

    def close(self):
        """Close an open project"""
        self.fail_on_closed()
        self.empty_project()

    def open(self, project_dir):
        """Open a new project"""
        self.dir = project_dir
        self.curr_sample = None
        meta = open(project_dir + "/project.ini", "r")
        self.num = int(meta.readline().split(" ")[1])
        self.title = meta.readline().strip()
        self.desc = meta.readline().strip()
        self.samples = []

        # Blank space
        meta.readline()

        sample = meta.readline().strip()
        while (sample != ""):
            if (sample.startswith("SAMPLE")):
                self.samples.append(Sample(project_dir + "/Samples/" + sample.split("\t")[1]))
            sample = meta.readline().strip()
        meta.close()

    def fail_on_closed(self):
        """If a project is closed and an action is called on it,
            raise an exception.
            """
        if self.dir is None:
            raise Exception("The project is closed")


class Sample:
    def __init__(self, sample_dir):
        self.__dir = sample_dir
        meta = open(sample_dir + "/sample.dat", "r")
        self.name = meta.readline().strip()
        self.diameter = float(meta.readline().strip())
        self.__disp_raw = []
        self.__load_raw = []
        line = meta.readline().strip()
        while line != "":
            disp, load = line.split("\t")
            self.__disp_raw.append(float(disp))
            self.__load_raw.append(float(load))
            line = meta.readline().strip()

    def __getitem__(self, ind):
        if (ind in range(len(self.__disp_raw))):
            return (self.__disp_raw[ind], self.__load_raw[ind])
        else:
            return None

    def get_disp_data(self):
        return self.__disp_raw

    def get_load_data(self):
        return self.__load_raw
