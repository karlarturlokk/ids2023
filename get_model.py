import os
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models import FastText
import PyPDF2

important_words = ['müügitulu', 'tulu', 'käive', 'kasum', 'puhaskasum', 'ärikasum']

pdf_directory = 'materjal'

accounting_sentences = []

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        except Exception as e:
            print(f"Error reading PDF file {pdf_path}: {e}")
            continue
        text = re.sub(r'[^a-zA-ZäõöüÄÕÖÜ\s]', '', text)
        sentences = [word_tokenize(sent.lower()) for sent in sent_tokenize(text)]
        accounting_sentences.extend([sentence for sentence in sentences if any(term in sentence for term in important_words)])

accounting_model = FastText(sentences=accounting_sentences, vector_size=300, window=5, min_count=5, workers=4, sg=1, epochs=10)

accounting_model.save('accounting_model_updated_v2.model')

for word in important_words:
    similar_words = accounting_model.wv.most_similar(word, topn=5)
    print(f"Similar words to {word}: {similar_words}")
