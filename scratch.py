import datetime

from app.project.project_dir import ProjectDirectory
from app.util.pdf import create_pdf, generate_sample_layer, generate_project_layer

proj = ProjectDirectory.open_project("C:/Users/egapx/PycharmProjects/RSGrapher/RSG 0002/")

date = datetime.datetime.utcnow()

generate_project_layer(proj.number, date.strftime("%B %d, %Y"), proj.template_file)
generate_sample_layer(proj.samples[0],
                      "C:/Users/egapx/PycharmProjects/RSGrapher/RSG 0002/pdfs for Test Report/temp/S1_INFO.pdf")

create_pdf("C:/Users/egapx/PycharmProjects/RSGrapher/RSG 0002/pdfs for Test Report/temp/S1_INFO.pdf",
           "C:/Users/egapx/PycharmProjects/RSGrapher/RSG 0002/pdfs for Test Report/graph_template.pdf",
           "C:/Users/egapx/PycharmProjects/RSGrapher/RSG 0002/pdfs for Test Report/temp/S1_PL.pdf",
           "out.pdf")