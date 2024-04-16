import pandas as pd

from dhlab import NER, POS

test_urn = "URN:NBN:no-nb_digibok_2021042748505"

def test_ner():
    target_res = pd.read_csv("tests/resources/ner_result.csv", index_col=0)
    res = NER(urn=test_urn, model="nb_core_news_sm", start_page=5, to_page=10)  
    assert target_res.equals(res.ner.iloc[:5])
    
def test_pos():
    target_res = pd.read_csv("tests/resources/pos_result.csv", index_col=0)
    pos = POS(urn=test_urn, model="nb_core_news_sm", start_page=500, to_page=510)
    assert target_res.equals(pos.pos.iloc[:5])
    