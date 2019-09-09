# importing required modules 
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
from io import BytesIO
from flask import *  
import os, math


def make_pdf_handout(pdfFileObj):
    # to store pdf byteArray
    pdf = BytesIO()

    # open the lines pdf
    linesFileObj = open('templates/notesField.pdf', 'rb')

    # creating a pdf Reader objects 
    pdfReader = PdfFileReader(pdfFileObj) 
    pdfLines = PdfFileReader(linesFileObj)

    # creating a pdf writer object for new pdf 
    pdfWriter = PdfFileWriter() 

    for pageNum in range(math.ceil(pdfReader.numPages/3)):
        # create blank page
        template_page = PageObject.createBlankPage(None, 850, 1100)
        # load the notes field
        notesPage = pdfLines.getPage(0)
        
        # add the pages that go in template
        for indx in range(0,3):
            pageIdx = pageNum*3+indx
            if pageIdx < pdfReader.numPages:
                pageObj = pdfReader.getPage(pageIdx)
                template_page.mergeScaledTranslatedPage(pageObj, 0.5, 60, 730-(330*indx), False)
                template_page.mergeScaledTranslatedPage(notesPage, 1, 480, 760-(330*indx), False)
            
        # adding template page object to pdf writer 
        pdfWriter.addPage(template_page) 
    # write the pdf into an IO Stream
    pdfWriter.write(pdf)
    return pdf


app = Flask(__name__)  
    
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
    
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        if not request.files.get('file', None):
            return redirect(url_for("upload"))
        else:
            pdf = make_pdf_handout(request.files['file'])
            response = make_response(pdf.getvalue())
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = "inline; filename=output.pdf"
            return response
       
    
if __name__ == '__main__':  
    app.run(debug = True)  