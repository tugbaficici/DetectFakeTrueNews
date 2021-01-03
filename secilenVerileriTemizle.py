#
# Bu temizleme işlemleri oluşturulan veri setlerinin daha iyi hesaplama yapılması adına ileri temizleme için kullanılmıştır
#
# İleri temizlemede aşağıda bulunan fonksiyonlar uygulanmıştır
# 
# 1-Rakamların yazıya çevrilmesi
# 2-N karakterden az kelimelerin temizlenmesi
# 3-SpellChecker ile kelime yazımlarını kontrol edip düzeltilmesi
# 4-Özel durumların temizlenmesi(Hashtag, kullanıcı etiketlemeleri)
# 5-Kelimelerin köklerinin bulunması
#
# Kullanılan setler= KullanilacakVeriler/LabelsizVeri/truetweets.csv-bilinclifaketweets.csv-bilincsizfaketweets.csv
#

import csv
import string
import re
from trnlp import SpellingCorrector,number_to_word,TrnlpWord

tweets = list()
tweetlist = list()

# Yazım kontrolü sağlayan fonksiyon tanımı
def spellcheck():
    obj = SpellingCorrector()
    for i in range(len(tweetlist)):
        obj.settext(tweetlist[i])
        kelimeler=(tweetlist[i]).split()
        sonuc=obj.correction(deasciifier=True,unrepeater=True,vowelizero=True)
        dogru=""
        for j in range(len(kelimeler)):
            try:
                dogru = dogru+sonuc[j][0]+" "
            except:
                pass
        if(dogru==""):
            dogru=tweetlist[i]
        print(dogru)
        tweetlist[i]=dogru+"\n"

# Kelimelerin köklerini bulan fonksiyon tanımı
def kokayirma():
    obj = TrnlpWord()
    for i in range(len(tweetlist)):
        kelimeler=tweetlist[i].split()
        cumle=""
        for j in kelimeler:
            obj.setword(j)
            sonuc=obj.get_stem
            if(sonuc==""):
                sonuc=j
            
            cumle=cumle+sonuc+" "
        if(cumle==""):
            cumle=tweetlist[i]
        else:
            tweetlist[i]=cumle+"\n"


# Rakamları yazıya çeviren fonksiyon tanımı
def numbertoword():
    for i in range(len(tweetlist)):
        stringsonuc=""
        numberlist=[int(s) for s in tweetlist[i].split() if s.isdigit()]
        for i in range(len(numberlist)):
            sonuc=number_to_word(str(numberlist[i]))
            tweetlist[i].find(str(numberlist[i]))
            stringsonuc=tweetlist[i].replace(str(numberlist[i]),sonuc)
        if(stringsonuc==""):
            pass
        else:
            tweetlist[i]=stringsonuc
        
# 3 ve daha küçük harften oluşan kelimeleri temizleyen fonksiyon tanımı
def ncharactersremove():
    for i in range(len(tweetlist)):
        tweetlist[i]=re.sub(r'\b\w{1,3}\b', '', tweetlist[i])
    
# Hashtag ve kullanıcı etiketlemelerini temizleyen fonksiyon tanımı
def specialcleaning():
    for i in range(len(tweetlist)):
        entity_prefixes = ['@','#']
        for separator in string.punctuation:
            if separator not in entity_prefixes :
                tweetlist[i] = tweetlist[i].replace(separator,' ')
        words = []
        for word in tweetlist[i].split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        tweetlist[i]= ' '.join(words)



# Temizlenecek veriler okunarak global listeye atıldı
# Temizlenecek verinin adının ve dosya yolunun değiştirilerek 3 veriseti içinde kullanılmıştır.
with open('KullanilacakVeriler/LabelsizVeri/truetweets.csv') as tweet:
    tweets = tweet.readlines()
    for i in tweets:
        tweetlist.append(i)

# Fonksiyonlar sırası ile çağırılarak uygulandı
specialcleaning()
print("#hashtag ve @kullanıcı'lar silindi")
spellcheck()
print("Yazım hataları giderildi")
ncharactersremove()
print("3 harf ve daha az olan kelimeler temizlendi")
kokayirma()
print("Kelime kökleri bulunarak tweetlere eklendi")
numbertoword()
print("Rakamlar yazıya dönüştürüldü")

# Yazım kontrolünün sonunda büyük harfa dönüştürülen ve tırnak eklenen tweetler 
# yeniden temizlendi
for i in range(len(tweetlist)):
    tweetlist[i]=tweetlist[i].lower()
    tweetlist[i] =tweetlist[i].replace("'", "")

# Verinin son hali belirtilen konuma yazdırıldı
# Çıktının adının ve dosya yolunun değiştirilerek 3 veriseti içinde kullanılmıştır.
with open('KullanilacakVeriler/LabelsizVeri/dogru.csv','w') as temizveri:
    for i in range(len(tweetlist)):
        temizveri.write(tweetlist[i])