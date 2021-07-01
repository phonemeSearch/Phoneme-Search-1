from icu import Locale, Collator
from functools import cmp_to_key
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


words = ['ἀγ', 'βλα', 'ὁμηρ', "ἀβε", "ἂέ", "ἂεδ"]
#san = ["", "", "", "", "", ""]

san = [
"abhakṣayam",
"abhakṣi",
"abhayaṃkaráḥ",
"abhicákṣe", "neṣatha",
"rákṣatha",
"tákṣatha",
"jújoṣatha",
"parṣatha",
"cétiṣṭha",
"yaviṣṭha",
"girvaṇastama",
"híraṇyavāśīmattama",
"tiṣṭhema",
"bhūṣema",
"sīṣadhāma",
"váṃsāma",
"kr̥ṇavāma",
"spr̥ṇavāma",
"śr̥ṇavāma"]

word = "śr̥ṇavāma"

san_trans = []
for word in san:
   san_trans.append(transliterate(word, sanscript.IAST, sanscript.DEVANAGARI))

loc = Locale('san')  # 'el' is the locale code for Greek

col = Collator.createInstance(loc)
sorted_words = sorted(san_trans, key=cmp_to_key(col.compare))

#print(sorted_words)

for word in sorted_words:
    #print(transliterate(word, sanscript.DEVANAGARI, sanscript.IAST))
    pass

#print(san)

deva = ["अ॒ग्निमी॑ळे", "पु॒रोहि॑तं", "य॒ज्ञस्य॑", "दे॒वमृ॒त्विज॑म्"]

iast_a = "hótāraṃ"
iast_b = "ratnadhā́tamam"

print(transliterate(iast_a, sanscript.IAST, sanscript.DEVANAGARI))
print(transliterate(iast_b, sanscript.ITRANS, sanscript.DEVANAGARI))

deva_res = []
def translit(res):
    for word in res:
       deva_res.append(transliterate(word, sanscript.IAST, sanscript.DEVANAGARI))
    return deva_res

    
translit(deva)