# Ülevaade
<br>
Projekt koosneb kolmest Pythoni failist. Kuna ettevõtete aastaaruanded on erineva ülesehitusega siis oli alguses plaanis kasutada OpenAI API-d. Esialgselt tegime pdf faili tükkidest ja genereerisime embeddingud, mille põhjal sai pärast keelemudelilt aruande kohta küsimusi küsida. Selline lähenemine põhimõtteliselt töötas kuid oli väga kulukas (üks päring maksis ligikaudu 10 senti) ja aruande koostamiseks on vaja mitmeid küsimusi. Samuti oli raskusi sellise lähenemisega tabelite koostamisel. Teiseks proovisime pythoni teeki PandasAI, mis võttis sisendiks kõik aruandes leiduvad tabelid ja vastas küsimustele neid arvestades. Selline lähenemine oli oluliselt vähem kulukas kuid umbes pooltele küsimustele ei osanud vastata. Viimaks proovisime aruandest kätte saada vajalikud tabelid kasutades pythoni teeki Camelot, mis loeb sisse kõik tabelid. Tabeli proovisime kätte saada nii, et kui näiteks kasumiaruande tabel algab alati lahtriga "Müügitulu", siis otsisime lihtsalt kõik tabelid läbi ja kui leidsime tabeli kus on lahter müügitulu, salvestasime selle. Selline lähenemine on tõenäoliselt kõige mõistlikum, kui on vaja kokkuvõttesse saada tabeleid. Hetkel on selle lähenemise miinuseks see, et kui tegu on suurettevõtetega, mille aruandes peavad olema nii kasumi kui ka konsolideeritud kasumi aruanded, siis programmi väljund on alati konsolideeritud kasumi tabel, sest mõlemas on lahter "Müügitulu" ja konsolideeritud kasumi tabel on alati viimane. Teiseks, tabelite ühendamisel vahetevahel programm millegipärast vahetab osade ridade järjekorra ära, mis tekitab raskusi tabelist arusaamisega. Arvatavasti on seda võimalik parandada kuid meie probleemist kahe tunniga jagu ei saanud.

<br>
Kokkuvõtteks võiks öelda, et kui tahta teha samasugust programmi, siis praegu tundub, et parim lähenemisviis oleks struktureeritud andmete töötlemiseks Camelotiga leida õiged tabeld, nad ühendada ja töödelda nii, et jääks vaid vajalikud parameetrid. Struktureerimata andmete puhul on raskem. Praegune parim lahendus on aruandest välja võtta kõik tekst (mitte tabelid), teha tekst mõstliku suurustega tükkideks ja jätta alles vaid tükid, mis sisaldavad vajalikke märksõnu. Seejärel teha embeddinguteks ja küsida keelemudelilt konkreetsele küsimusele vastust. Ilmsalt tuleks keelemudelit ka fine-tuneda, sest vastused olid enamasti küll õiged, kuid väga erineva struktuuriga.

<br>
get_model.py
Skript loeb PDF-faile kindlaksmääratud kataloogist ja loeb teksti igalt lehelt. Seejärel keskendub skript lausetele, mis sisaldavad olulisi märksünu nagu 'müügitulu', 'tulu', 'käive', 'kasum', 'puhaskasum' ja 'ärikasum'. Nende lõikudega treenitakse FastText mudel.

<br>
pdf_lugemine.py
See skript kasutab varemtreenitud FastText mudelit, et vastata küsimustele PandasAI SmartDataframe-i põhjal.

<br>
get_tabelid.py
Võtab sisendiks, järjendi aruannetest, ning leiab igast aruandest üles käive ja bilansi tabelid, töötleb neid ja ühendab aastate lõikes. Väljundiks on PDF genereeritud tabelitega.

<br>
UUS poster B11.png
Poster, mis oli ka Deltas postrisessioonil. (Printisime ise välja)

<br>
NÄIDIS Ettevõte 5 aasta ülevaade.pdf
Näidis get_tabelid.py tööst. Sisendiks Arnika OÜ viie viimase aasta aastaaruanded.
