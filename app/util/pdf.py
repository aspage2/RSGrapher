from PyPDF2.pdf import PageObject
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image

LOGO_WIDTH = 150
LOGO_MARGIN = 0

TEXT_MARGIN = 30


def generate_project_layer(proj_num, proj_date, pdf_dir):
    """Layer 1: PROJECT (logo, project number, date)"""
    proj_num_str = "RSG {:0>4}".format(proj_num)
    lwidth, lheight = Image.open("res/logo.png").size
    drawwidth = LOGO_WIDTH
    drawheight = int(LOGO_WIDTH * lheight / lwidth)
    pagewidth, pageheight = landscape(letter)
    c = canvas.Canvas(pdf_dir, pagesize=(pagewidth, pageheight))

    c.setFillColor("#282560")
    c.setFont("Helvetica-Bold", 16)
    c.drawImage(
        ImageReader("res/logo.png"),
        LOGO_MARGIN,
        pageheight - drawheight - LOGO_MARGIN,
        width=drawwidth,
        height=drawheight,
        mask="auto",
    )
    c.drawString(TEXT_MARGIN, TEXT_MARGIN, proj_date)
    c.drawRightString(
        pagewidth - TEXT_MARGIN, pageheight - 16 - TEXT_MARGIN, proj_num_str
    )
    c.showPage()
    c.save()


TITLE_SHIFT_FACTOR = 30
TITLE_FONT = 16
SUBTITLE_FONT = 14


def generate_sample_layer(sample, filename):
    """Layer 2: SAMPLE (sample #, titles)"""
    sample_num_str = "Sample #{}".format(sample.num)
    pagewidth, pageheight = landscape(letter)
    c = canvas.Canvas(filename, pagesize=(pagewidth, pageheight))
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(
        pagewidth - TEXT_MARGIN, pageheight - 35 - TEXT_MARGIN, sample_num_str
    )

    titles = sample.titles
    c.setFont("Helvetica-Bold", TITLE_FONT)
    c.drawCentredString(
        pagewidth / 2 + TITLE_SHIFT_FACTOR,
        pageheight - TITLE_FONT - TEXT_MARGIN,
        titles[0],
    )
    i = 1
    c.setFont("Helvetica", SUBTITLE_FONT)
    c.setFillColor("#6d6d6d")
    while i < len(titles):
        c.drawCentredString(
            pagewidth / 2 + TITLE_SHIFT_FACTOR,
            pageheight - TITLE_FONT - (SUBTITLE_FONT + 3) * i - TEXT_MARGIN,
            titles[i],
        )
        i += 1
    c.showPage()
    c.save()


GRAPH_SCALE_FACTOR = 1.1


def create_pdf(sample_file, template_file, graph_file, out_file, num_titles=None):
    # Open generated PDF's
    template = PdfFileReader(open(template_file, "rb")).getPage(0)
    graph = PdfFileReader(open(graph_file, "rb")).getPage(0)
    sample_layer = PdfFileReader(open(sample_file, "rb")).getPage(0)

    # Calculate graph offset
    dx = int(
        (
            template.mediaBox.getWidth()
            - GRAPH_SCALE_FACTOR * int(graph.mediaBox.getWidth())
        )
        / 2
    )
    dy = int(
        (
            template.mediaBox.getHeight()
            - GRAPH_SCALE_FACTOR * int(graph.mediaBox.getHeight())
        )
        / 2
    )

    # Merge layers
    out = PageObject.createBlankPage(
        None, template.mediaBox.getWidth(), template.mediaBox.getHeight()
    )
    out.mergeScaledTranslatedPage(graph, GRAPH_SCALE_FACTOR, dx, dy - 20)
    out.mergePage(sample_layer)
    out.mergePage(template)

    # Write
    w = PdfFileWriter()
    w.addPage(out)
    with open(out_file, "wb") as f:
        w.write(f)
