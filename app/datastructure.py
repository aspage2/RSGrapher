import os

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


## Create a project with the given parameters in the given directory
##  Set up file structure and meta data file
def create_project(directory, project_title, project_num, project_desc):
    file_location = directory + "\\RSG " + str(project_num) + " - " + project_title
    os.mkdir(file_location)
    os.mkdir(file_location + "\\Samples")
    os.mkdir(file_location + "\\Photos")
    os.mkdir(file_location + "\\pdfs for Test Report")
    os.mkdir(file_location + "\\Excel Data")
    os.mkdir(file_location + "\\Stress Strain Data")
    meta_file = open(file_location + "\\project.ini", "w+")
    meta_file.write("RSG " + str(project_num) + "\n")
    meta_file.write(project_title + "\n")
    meta_file.write(project_desc + "\n")
    meta_file.close()


class Project:
    def __init__(self, project_dir):
        self.__dir = project_dir
        meta = open(project_dir + "\\project.ini", "r")
        self.num = int(meta.readline().split(" ")[1])
        self.title = meta.readline().strip()
        self.desc = meta.readline().strip()
        self.__samples = []
        sample = meta.readline().strip()
        while (sample != ""):
            if (sample.startswith("SAMPLE")):
                self.__samples.append(Sample(project_dir + "\\Samples\\" + sample.split("\t")[1]))
            sample = meta.readline().strip()
        meta.close()

    def samples(self):
        return self.__samples

    def get_sample(self, i):
        if (i in range(len(self.__samples))):
            return self.__samples[i]
        else:
            return None

    def add_sample(self, name, ascdata):
        sample_dir = self.__dir + "\\Samples\\" + name

        ## Setup sample directory in the project structure
        os.mkdir(sample_dir)
        data = open(sample_dir + "\\sample.dat", "w+")
        data.write(name + "\n")
        for i in range(len(ascdata)):
            disp, load = ascdata[i]
            data.write(str(disp) + "\t" + str(load) + "\n")
        data.close()

        ## Add sample to project.ini
        project_meta = open(self.__dir + "\\project.ini", "a")
        project_meta.write("SAMPLE\t" + name + "\n")
        project_meta.close()


class Sample:
    def __init__(self, sample_dir):
        self.__dir = sample_dir
        meta = open(sample_dir + "\\sample.dat", "r")
        self.name = meta.readline().strip()
        self.__disp_raw = []
        self.__load_raw = []
        line = meta.readline().strip()
        while (line != ""):
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
