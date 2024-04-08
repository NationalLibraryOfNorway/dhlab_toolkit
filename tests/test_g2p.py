# %%
from convert_pa import nofabet_to_ipa, nofabet_to_sampa
from dhlab_toolkit.g2p.g2p_models import transcribe

# %%
def test_transcribe(): 
    text = "I Nasjonalbiblioteket har vi veldig mange gamle og sjeldne bøker"
    
    expected_output = """I|II1|"i:|'ɪː
Nasjonalbiblioteket|N AH0 SJ OH0 N AA1 L B IH0 B L IH0 OH0 T EE3 K AX0|nA$SU$"nA:l$bI$blI$U$%te:$k@|nɑ.ʃʊ.'nɑːl.bɪ.blɪ.ʊ.ˌteː.kə
har|H AA1 R|"hA:r|'hɑːr
vi|V IH0|vI|vɪ
veldig|V EH2 L D IH0|""vEl$dI|"vɛl.dɪ
mange|M AH2 NG AX0|""mAN$@|"mɑŋ.ə
gamle|G AH2 M L AX0|""gAm$l@|"gɑm.lə
og|OA1|"o:|'oː
sjeldne|SJ EH2 L D N AX0|""SEld$n@|"ʃɛld.nə
bøker|B OE2 K AX0 R|""b2:$k@r|"bøː.kər""".splitlines()

    transcription = list(transcribe(text))#.split()))

    for i, (word, nofabet) in enumerate(transcription):
       # nofabet = " ".join(pronunciation)
        ipa = nofabet_to_ipa(nofabet)
        sampa = nofabet_to_sampa(nofabet)
        result = "|".join((word, nofabet,sampa, ipa))
        print(result)
        assert result == expected_output[i]

#%%
