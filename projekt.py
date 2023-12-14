import camelot
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import os

os.environ["OPENAI_API_KEY"] = ""

desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 100)


def pdfTekstiks(pdf_list):
    tekst = ""
    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        for leht in pdf_reader.pages:
            tekst += leht.extract_text()
    return tekst


def hakiTekst(tekst):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
    teksti_tükid = text_splitter.split_text(tekst)
    return teksti_tükid


def embedding(teksti_tükid):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=teksti_tükid, embedding=embeddings)
    return vectorstore


def loeTabelid(pdflist):
    tabelid_sõnastik = {}
    for pdf in pdflist:
        tabelid = camelot.read_pdf(pdf, pages='all')
        for i, tabel in enumerate(tabelid):
            if 'Müügitulu' in tabel.df.values:
                tabelid_sõnastik['Kasum_'+str(pdf.split('_')[len(pdf.split('_'))-1][:4])] = tabel.df
            if 'Varad' in tabel.df.values:
                tabelid_sõnastik['Bilanss'+str(pdf.split('_')[len(pdf.split('_'))-1][:4])] = tabel.df
    return tabelid_sõnastik

def töötleTabelid(tabelid):
    bilansid = []
    kasumid = []
    for key in tabelid:
        if 'Bilanss' in key:
            bilansid.append(tabelid.get(key))
        if 'Kasum' in key:
            kasumid.append(tabelid.get(key))
    for i in range(len(bilansid) - 1):
        if i == 0:
            bilansid_kokku = pd.merge(bilansid[i], bilansid[i + 1], on=0, how='outer', suffixes=(str(i), str(i + 1)))
        else:
            bilansid_kokku = pd.merge(bilansid_kokku, bilansid[i + 1], on=0, how='outer', suffixes=(str(i), str(i + 1)))
    bilansid_kokku = bilansid_kokku[remove_duplicate_values(bilansid_kokku.iloc[0].to_dict()).keys()].drop_duplicates()
    for i in range(len(kasumid) - 1):
        if i == 0:
            kasumid_kokku = pd.merge(kasumid[i], kasumid[i + 1], on=0, how='outer', suffixes=(str(i), str(i + 1)))
        else:
            kasumid_kokku = pd.merge(kasumid_kokku, kasumid[i + 1], on=0, how='outer', suffixes=(str(i), str(i + 1)))
    kasumid_kokku = kasumid_kokku[remove_duplicate_values(kasumid_kokku.iloc[0].to_dict()).keys()].drop_duplicates()
    pealised_kasumid = kasumid_kokku.iloc[0]
    pealised_bilansid = bilansid_kokku.iloc[0]
    return [pd.DataFrame(kasumid_kokku.values[1:], columns=pealised_kasumid),
            pd.DataFrame(bilansid_kokku.values[1:], columns=pealised_bilansid)]


def remove_duplicate_values(input_dict):
    reverse_dict = {}
    result_dict = {}
    for key, value in input_dict.items():
        if value not in reverse_dict:
            result_dict[key] = value
            reverse_dict[value] = key
    return result_dict

def koostaPDF(firmanimi, periood,tabelid):
    filename = firmanimi + ' ' + str(periood) + ' aasta ülevaade.pdf'
    document_title = firmanimi + ' ' + str(periood) + ' aasta ülevaade'

    pdf = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    tabel_bilanss = [tabelid[1].columns.to_list()] + tabelid[1].values.tolist()
    tabel_kasum = [tabelid[0].columns.to_list()] + tabelid[0].values.tolist()

    kasum = Table(tabel_kasum)
    kasum.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#d0d0d0'),
                               ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
                               ('GRID', (0, 0), (-1, -1), 1, '#000000')]))

    bilanss = Table(tabel_bilanss)
    bilanss.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#d0d0d0'),
                                 ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                 ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
                                 ('GRID', (0, 0), (-1, -1), 1, '#000000')]))

    title = Paragraph(f'<font size="18">{document_title}</font>', getSampleStyleSheet()['Heading2'])
    text1_kasum = Paragraph("Kasum", getSampleStyleSheet()['Normal'])
    text2_bilanss = Paragraph("Bilanss", getSampleStyleSheet()['Normal'])

    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(text1_kasum)
    elements.append(Spacer(1, 12))
    elements.append(kasum)
    elements.append(Spacer(1, 12))
    elements.append(text2_bilanss)
    elements.append(Spacer(1, 12))
    elements.append(bilanss)
    pdf.build(elements)
    return


pdf = [r"C:\Users\artur\Desktop\Arnika_Taheteenused_OU-aruanne_2019.pdf",
       r"C:\Users\artur\Desktop\Arnika_Taheteenused_OU-aruanne_2020.pdf",
       r"C:\Users\artur\Desktop\Arnika_Taheteenused_OU-aruanne_2021.pdf",
       r"C:\Users\artur\Desktop\Arnika_Taheteenused_OU-aruanne_2022.pdf"]

# pdf = [r"C:\Users\artur\Desktop\Prike_Group_OU-aruanne_2022.pdf",
#        r"C:\Users\artur\Desktop\Prike_Group_OU-aruanne_2021.pdf"]

tabelid = loeTabelid(pdf)
print(tabelid)
töödeldud_tabelid = töötleTabelid(tabelid)
koostaPDF('ettevõte',5,töödeldud_tabelid)