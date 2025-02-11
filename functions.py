import base64
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Table, TableStyle
from pypdf import PdfWriter, PdfReader
import os
import numpy as np
from streamlit_pdf_viewer import pdf_viewer


page_width = 595
page_height = 420


def create_pdf(data):
    filename = f"PDFs/{data['name']}_{data['month']}_{data['year'].astype('str')}_salary-slip.pdf"

    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    img_file = "img.jpg"

    img_width = 130
    x_start = (page_width/2) - (img_width/2) -12
    y_start = page_height - 125
    c.drawImage(img_file, x_start, y_start, img_width, preserveAspectRatio=True)

    # Address
    text_address = "210-211, Rudram Icon, Opp. LAMBDA Research Center, Gota, Ahmedabad-382481"
    text_address_width = c.stringWidth(text_address , "Helvetica", 12)
    c.setFont("Helvetica", 12)
    c.drawString((page_width/2) - (text_address_width/2), 320, text_address)

    # Payslip : [DATE]

    month = data['month']
    year = data['year'].astype('str')

    text_payslip = f"Pay Slip : {month} - {year}"
    text_payslip_width = c.stringWidth(text_payslip , "Helvetica", 12)
    c.setFont("Helvetica-Bold", 10)
    c.drawString((page_width/2) - (text_payslip_width/2), 300, text_payslip)

    # Sign
    text_line = "_"*25
    text_line_width = c.stringWidth(text_line , "Helvetica", 12)
    c.setFont("Helvetica", 12)
    c.drawString((page_width/2) + (text_line_width/2), 65, text_line)

    # sign-text
    text_sign = "Employer Signature"
    text_sign_width = c.stringWidth(text_sign , "Helvetica-Bold", 12)
    c.setFont("Helvetica-Bold", 12)
    c.drawString((page_width/2) + (text_line_width/2) + (text_sign_width/4), 45, text_sign)

    details = [
        ["Name", data['name'].capitalize() ],
        ["ID", data['id']],
        ["Designation", data['designation']],
        ["Date of Leaving", data['date_of_leaving']],
        ["Net Salary", data["net_salary"].astype('float64')],
        ["Incentive Pay", data["incentive_pay"].astype('float64')],
        ["Gross Salary", data["gross_salary"].astype('float64')],
        ["Amount in Words", data["amount_in_words"]],
    ]

    table = Table(details, colWidths=[170, 230])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.white),
        ("TEXTCOLOR", (0, 0), (1, 0), colors.black),   
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    table.wrapOn(c, 97.5, 120)
    table.drawOn(c, 97.5, 120)
    c.showPage()
    # print(type(c))
    c.save()
    return filename

def save_pdf(pdf_names):
    # merge pdfs
    merger = PdfWriter()
    for pdf_name in pdf_names:
        if os.path.exists(pdf_name):
            try:
                merger.append(pdf_name)
            except Exception as e:
                print(f"Error appending {pdf_name}: {e}")
        else:
             print(f"File not found: {pdf_name}")
    
    output_path = "PDFs/output.pdf"
    merger.write(output_path)
    merger.close()

    #delete files
    for pdf_name in pdf_names:
        if os.path.exists(pdf_name):
            try:
                os.remove(pdf_name)
            except Exception as e:
                # print(f"Error appending {pdf_name}: {e}")
                pass
        else:
            #  print(f"File not found: {pdf_name}")
            pass

def displayPDF(file):
    st.write("first")
    with open(file, "rb") as f:
        st.write("second")
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    st.write("third")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    st.write("fourth")
    st.markdown(pdf_display, unsafe_allow_html=True)
    # st.components.v1.html(pdf_display, height=900)

