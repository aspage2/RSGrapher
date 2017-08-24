
import pylatex as tex

def gen_pdf(imgfile, pdfdir):
    tex.Document()
    doc = tex.Document(default_filepath="C:\\Users\\egapx\\Desktop\\RSG344 - My Project\\Pdfs\\")
    doc.documentclass = tex.Command("documentclass", options=['12pt','landscape'],arguments=['article'])
    f = tex.Figure(position="h")
    f.add_image("C:\\Users\\egapx\\Desktop\\RSG344 - My Project\\Graphs\\S1_YL.png",width="textwidth")
    print("WAT")
    doc.create(f)
    doc.generate_pdf("full")
