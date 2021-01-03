#
# Denenecek cümle için hızlı bir temizleme işlemi yapılması adına bu dosya oluşturulmuştur.
#
# Fonksiyonlar
# 
# 1-Noktalama işaretlerinin temizlenmesi
# 2-Küçük harfe dönüştürülmesi
# 3-Etkisiz kelimelerin temizlenmesi
# 4-Yazım yanlışı kontrolü
# 5-N karakterden az kelimelerin silinmesi
# 6-Kelime köklerinin ayrılması
#

import csv
import string
import re
from trnlp import SpellingCorrector,number_to_word,TrnlpWord

turkçeStopWords=['acaba','ama','artık','asla','aslında','az','ancak',
            'bana','bazen','bazı','bazıları', 'bazısı', 'belki', 'ben', 'beni','benim', 'beş',
            'bile', 'bir', 'birçoğu', 'birçok', 'birçokları','biri', 'birisi', 'birkaç', 'birkaçı',
            'birşey', 'birşeyi', 'biz','bize', 'bizi', 'bizim', 'böyle', 'böylece', 'bu', 'buna',
            'bunda', 'bundan', 'bunu','bunun', 'burada', 'bütün',
            'çoğu', 'çoğuna', 'çoğunu', 'çok', 'çünkü',
            'da', 'daha', 'de', 'değil', 'demek', 'diğer', 'diğeri', 'diğerleri', 'diye', 'dolayı',
            'elbette', 'en',
            'fakat', 'falan', 'felan', 'filan',
            'gene', 'gibi',
            'hangi', 'hangisi', 'hani', 'hatta', 'hem', 'henüz', 'hep', 'hepsi', 'hepsine', 'hepsini',
            'her', 'her biri', 'herkes', 'herkese', 'herkesi', 'hiç', 'hiç kimse', 'hiçbiri', 'hiçbirine', 'hiçbirini',
            'için', 'içinde', 'ile', 'ise', 'işte',
            'kaç', 'kadar', 'kendi', 'kendine', 'kendini', 'ki', 'kim', 'kime', 'kimi', 'kimin', 'kimisi',
            'madem', 'mı', 'mi', 'mu', 'mü',
            'nasıl', 'ne', 'ne kadar', 'ne zaman', 'neden', 'nedir', 'nerde', 'nerede', 'nereden', 'nereye', 'nesi', 'neyse', 'niçin', 'niye',
            'ona', 'ondan', 'onlar', 'onlara', 'onlardan', 'onların', 'onu', 'onun', 'orada', 'oysa', 'oysaki',
            'öbürü', 'ön', 'önce', 'ötürü', 'öyle',
            'sana', 'sen', 'senden', 'seni', 'senin', 'siz', 'sizden', 'size', 'sizi', 'sizin', 'son', 'sonra',
            'şayet', 'şey', 'şimdi', 'şöyle', 'şu', 'şuna', 'şunda', 'şundan', 'şunlar', 'şunu', 'şunun',
            'tabi', 'tamam', 'tüm', 'tümü',
            'üzere',
            'var', 've', 'veya', 'veyahut',
            'ya', 'ya da', 'yani', 'yerine', 'yine', 'yoksa',
            'zaten', 'zira']

punctuation = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'"]

def cumleTemizle(cumle):
    #Aşama 1-Noktalama işaretleri, Büyük harflerin küçültülmesi
    cumle=cumle.lower()
    yenicumle = ""
    for j in cumle:
        if j not in punctuation:
            yenicumle += j
    cumle=yenicumle

    #Aşama 2-Etkisiz kelimeler(stopwords):
    kelimeler=cumle.split(" ")
    yenicumle = ""
    for j in kelimeler:
        if j not in turkçeStopWords:
            yenicumle += j+" "
    cumle=yenicumle

    #Aşama 3-Yazım kontrolü
    obj = SpellingCorrector()
    obj.settext(cumle)
    kelimeler=(cumle).split()
    sonuc=obj.correction(deasciifier=True,unrepeater=True,vowelizero=True)
    dogru=""
    for j in range(len(kelimeler)):
        try:
            dogru = dogru+sonuc[j][0]+" "
        except:
            pass
    if(dogru==""):
        dogru=cumle
    cumle=dogru

    #Aşama 4-N karakter temizlenmesi
    cumle=re.sub(r'\b\w{1,3}\b', '', cumle)

    #Aşama 4-Kök ayırma
    obj = TrnlpWord()
    kelimeler=cumle.split()
    yenicumle=""
    for j in kelimeler:
        obj.setword(j)
        sonuc=obj.get_stem
        if(sonuc==""):
            sonuc=j            
        yenicumle=yenicumle+sonuc+" "
    if(yenicumle==""):
        yenicumle=cumle
    else:
        cumle=yenicumle
    
    return cumle
