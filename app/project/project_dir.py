import os

class ProjectDirectory:
    """Representation of the directory of a Project"""

    def __init__(self, title, number, directory):
        self.title = title
        self.number = number
        self.directory = directory

    @property
    def sample_dir(self):
        """Helper method returning the sample directory for this project"""
        return self.directory + "/Samples/"

    @property
    def photo_dir(self):
        return self.directory + "/Photos/"

    @property
    def graph_dir(self):
        return self.directory + "/Graphs/"

    @staticmethod
    def create_project(title, number, parent_dir):
        """Create a project and write it to [parent_dir]/RSG[number] - [title]"""
        proj_dir = "{}/RSG{} - {}".format(parent_dir, number, title)
        os.mkdir(proj_dir)
        os.mkdir(proj_dir+"/Samples")
        os.mkdir(proj_dir+"/Graphs")
        os.mkdir(proj_dir+"/Photos")
        os.mkdir(proj_dir+"/Pdfs")
        ret = ProjectDirectory(title,number,proj_dir)
        return ret
