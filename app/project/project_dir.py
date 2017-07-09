import os
import json

from app.project.sample import Sample

class ProjectDirectory:
    """Representation of the directory of a Project"""

    def __init__(self, title, number, directory):
        self.title = title
        self.number = number
        self.directory = directory
        self.kwinfo = {}
        self.kwinfo_modified = False
        self.samples = []

    def sample_dir(self):
        """Helper method returning the sample directory for this project"""
        return self.directory + "/Samples/"

    def update_kwinfo(self, **kwargs):
        """Update the kwinfo attribute with new key value pairs"""
        for key, value in kwargs.items():
            self.kwinfo[key] = value
        self.kwinfo_modified = True

    def add_new_sample(self, name, area, data):
        """Add a sample to the project"""
        self.dirtysamples.append(Sample(name, area, data, self.sample_dir()))

    def mark_sample_as_dirty(self, sample):
        """Mark a sample as modified"""
        if sample in self.samples:
            self.dirtysamples.append(sample)

    def up_to_date(self):
        """All changes have been written back to the filesystem"""
        return len(self.dirtysamples) == 0

    def as_dict(self):
        """Serializable representation of a project"""
        return {"title":self.title,
               "number":self.number,
               "directory":self.directory,
               "kwinfo":self.kwinfo,
               "samples":[s.as_dict() for s in self.samples]}

    def write(self):
        """Write changes to """
        # resolve any new samples
        while len(self.dirtysamples) > 0:
            s = self.dirtysamples.pop()
            s.write_data()
            if s not in self.samples:
                self.samples.append(s)
        with open(self.directory+"/project.json",'w') as fh:
            json.dump(self.as_dict(), fh)
            kwinfo_modified = False

    @staticmethod
    def open(directory):
        """Open the project given its root directory"""
        with open(directory+"/project.json",'r') as fh:
            data = json.load(fh)
            ret = ProjectDirectory(data['title'],data['number'],data['directory'])
            ret.update_kwinfo(**data['kwinfo'])
            for s in data['samples']:
                ret.samples.append(Sample.from_dict(**s))
        return ret

    @staticmethod
    def create_project(title, number, parent_dir):
        """Create a project and write it to [parent_dir]/RSG[number] - [title]"""
        proj_dir = parent_dir + "/RSG"+number+" - "+title
        os.mkdir(proj_dir)
        os.mkdir(proj_dir+"/Samples")
        os.mkdir(proj_dir+"/Pdfs")
        os.mkdir(proj_dir+"/Photos")

        ret = ProjectDirectory(title,number,proj_dir)
        ret.write()
        return ret
