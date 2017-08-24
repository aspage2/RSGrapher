
import fpdf

def gen_pdf(imgfile, pdffile):
    pdf = fpdf.FPDF()
    pdf.add_page("Landscape")
    pdf.image(imgfile,w=270,y=20)
    pdf.output(pdffile)
