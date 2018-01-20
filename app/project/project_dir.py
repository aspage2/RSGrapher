import os
import json

from app.project.sample import Sample

DATA_FOLDER = "Raw Data/"
PHOTO_FOLDER = "Photos/"
PDF_FOLDER = "pdfs for Test Report/"
class ProjectDirectory:
    """Data class for Project info (directory, title, sample list)"""

    def __init__(self, title, number, directory):
        self.title = title
        self.number = number
        self._directory = directory
        self.samples = []

    def add_sample(self, sample):
        self.samples.append(sample)

    def add_blank_sample(self):
        self.samples.append(Sample())

    def delete_sample(self, sample):
        self.samples.remove(sample)

    @property
    def has_samples(self):
        return len(self.samples) != 0

    @property
    def root(self):
        return self._directory

    @property
    def data_dir(self):
        """Helper method returning the sample directory for this project"""
        return self._directory + DATA_FOLDER

    @property
    def photo_dir(self):
        return self._directory + PHOTO_FOLDER

    @property
    def pdf_dir(self):
        return self._directory + PDF_FOLDER

    def write_project(self):
        data = {'title': self.title, 'number': self.number}
        samples = []
        for sample in self.samples:
            samples.append(sample.json)
        data['samples'] = samples
        with open(self.root + "project.json", 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def create_project(title, number, proj_dir):
        """Create a project and write it to [parent_dir]/RSG[number] - [title]"""
        os.mkdir(proj_dir + DATA_FOLDER)
        os.mkdir(proj_dir + PHOTO_FOLDER)
        os.mkdir(proj_dir + PDF_FOLDER)
        ret = ProjectDirectory(title,number,proj_dir)
        return ret

    @staticmethod
    def open_project(proj_dir):
        with open(proj_dir+"project.json", 'r') as f:
            data = json.loads(f.read())
            ret = ProjectDirectory(data['title'], data['number'], proj_dir)
            for sample in data['samples']:
                ret.add_sample(Sample.from_json(sample))
        return ret