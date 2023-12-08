import tabula
import pandas as pd
#from pandasai import*
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
llm = OpenAI(api_token='võti')


dfs = tabula.read_pdf("NOTE_Parnu_OU-aruanne_2022.pdf", stream=True, pages='all')
#print(len(dfs))
#print(dfs[0])

df = SmartDataframe(dfs[0], config={"llm": llm})
vaste = df.chat('mis on firma aastakasumid ja vahemikud, järjesta aastate järgi kasvavalt')

vaste.to_csv('tabel.csv')
