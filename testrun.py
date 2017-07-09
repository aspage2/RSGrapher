
from app.util.asc_data import ASCData

a = ASCData.open("samples/rawdata.asc")

from app.project.project_dir import ProjectDirectory
from app.project.sample import Sample

p = ProjectDirectory.open("/home/alex/RSG500 - PNP Test Project")

p.add_new_sample("Wat", 500.0, a)

p.write()