import tabula
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from gensim.models import FastText
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

accounting_model = FastText.load('accounting_model_updated_v2.model')

llm = OpenAI(api_token='OPENAI_KEY')

words = ['müügitulu']
similar_words = set()

for word in words:
    similar_words.update(accounting_model.wv.most_similar(word, topn=5))

similar_words = [word[0] for word in similar_words]

fail = "NOTE_Parnu_OU-aruanne_2020.pdf"
dfs = tabula.read_pdf(fail, stream=True, pages='all')

filtered_dfs = []
for df in dfs:
    df_text = ' '.join(df.astype(str).values.flatten()).lower()
    if any(keyword in df_text or keyword in similar_words for keyword in words):
        filtered_dfs.append(df)

ranked_dataframes = []
vectorizer = CountVectorizer().fit([' '.join(words)])

for df in filtered_dfs:
    df_text = ' '.join(df.astype(str).values.flatten()).lower()
    df_vector = vectorizer.transform([df_text])
    question_vector = vectorizer.transform([' '.join(words)])
    similarity_score = cosine_similarity(df_vector, question_vector)[0][0]
    ranked_dataframes.append((df, similarity_score))

top_3_dataframes = sorted(ranked_dataframes, key=lambda x: x[1], reverse=True)[:3]
final_dataframes = [df for df, _ in top_3_dataframes]

sdfs = []
for df in final_dataframes:
    sdf = SmartDataframe(df, config={"llm": llm})
    sdfs.append(sdf)

question = "Palun anna üksikasjalik ülevaade firma aastakasumitest aastate lõikes. Maini igal aastal saadud kasumit ja selgitage, millised olid peamised kasvusuundumused või muutused aastate jooksul. Firma aastakasumid aastate kaupa:"

responses = []
for sdf in sdfs:
    response = sdf.chat(question)
    responses.append(response)

print(responses[0])
print(responses[1])
