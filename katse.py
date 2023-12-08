import tabula
import pandas as pd
#from pandasai import*
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from gensim.models import fasttext
from gensim.test.utils import datapath
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#model = fasttext.load_facebook_vectors(datapath(r'C:\Users\School\PycharmProjects\SAT\cc.et.300.bin'))

llm = OpenAI(api_token='võti')
#pandas_ai = PandasAI(llm, verbose=True, conversational=True)

dfs = tabula.read_pdf("NOTE_Parnu_OU-aruanne_2022.pdf", stream=True, pages='all')

filtered_dfs = []

question = 'mis on firma aastakasumid ja vahemikud, järjesta aastate järgi kasvavalt'
for df in dfs:
    # Check if the question keywords are present in the DataFrame text
    df_text = ' '.join(df.astype(str).values.flatten()).lower()
    if any(keyword in df_text for keyword in question.split()):
        filtered_dfs.append(df)

ranked_dataframes = []
vectorizer = CountVectorizer().fit([question])

for df in filtered_dfs:
    df_text = ' '.join(df.astype(str).values.flatten()).lower()
    df_vector = vectorizer.transform([df_text])
    question_vector = vectorizer.transform([question])
    similarity_score = cosine_similarity(df_vector, question_vector)[0][0]
    ranked_dataframes.append((df, similarity_score))

top_5_dataframes = sorted(ranked_dataframes, key=lambda x: x[1], reverse=True)[:5]
final_dataframes = [df for df, _ in top_5_dataframes]
sdfs = []

for df in final_dataframes:
    sdf = SmartDataframe(df, config={"llm": llm})
    sdfs.append(sdf)


for sdf in sdfs:
    print(sdf.chat(question))
"""
# DataFrame to PDF
# See on mingi täielik jura
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pdf_filename = 'output.pdf'
with PdfPages(pdf_filename) as pdf:
    fig, ax = plt.subplots()
    ax.axis('off')  # Turn off axis
    table_data = [vaste.columns] + vaste.values.tolist()
    table = ax.table(cellText=table_data, loc='center', colLabels=None, cellLoc='center')
    pdf.savefig()
    plt.close()

print(f'DataFrame has been exported to {pdf_filename}')
"""
