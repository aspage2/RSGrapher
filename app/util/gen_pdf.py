from PyPDF2.pdf import PageObject
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

LOGO_WIDTH = 150
LOGO_MARGIN = 0

TEXT_MARGIN = 30

def graph_page_template(proj_num, proj_date, pdf_dir):
    """Draw the overlay template for the final graph PDF output"""
    proj_num_str = "RSG {:0>4}".format(proj_num)
    lwidth, lheight = Image.open("res/logo.png").size
    drawwidth = LOGO_WIDTH
    drawheight = int(LOGO_WIDTH * lheight / lwidth)
    pagewidth, pageheight = landscape(letter)
    c = canvas.Canvas(pdf_dir, pagesize=(pagewidth, pageheight))
    c.setFont("Helvetica-Bold", 16)
    c.drawImage(ImageReader("res/logo.png"), LOGO_MARGIN, pageheight - drawheight - LOGO_MARGIN, width=drawwidth,
                height=drawheight, mask="auto")
    c.drawString(TEXT_MARGIN,TEXT_MARGIN,proj_date)
    c.drawRightString(pagewidth-TEXT_MARGIN, pageheight-12-TEXT_MARGIN, proj_num_str)
    c.showPage()
    c.save()

GRAPH_SCALE_FACTOR = 1.1

def create_pdf(template_file, graph_file, out_file):
    template = PdfFileReader(open(template_file, 'rb')).getPage(0)
    graph = PdfFileReader(open(graph_file,'rb')).getPage(0)
    dx = int((template.mediaBox.getWidth() - GRAPH_SCALE_FACTOR*int(graph.mediaBox.getWidth()))/2)
    dy = int((template.mediaBox.getHeight() - GRAPH_SCALE_FACTOR*int(graph.mediaBox.getHeight()))/2)

    out = PageObject.createBlankPage(None, template.mediaBox.getWidth(), template.mediaBox.getHeight())
    out.mergeScaledTranslatedPage(graph, GRAPH_SCALE_FACTOR, dx, dy)
    out.mergePage(template)

    w = PdfFileWriter()
    w.addPage(out)
    with open(out_file, 'wb') as f:
        w.write(f)
