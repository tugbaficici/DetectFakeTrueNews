#
# Bu temizleme işlemleri doğru yanlış veri kümelerinin daha iyi ayrılması için kullanılmıştır
#
# Temizlemede aşağıda bulunan fonksiyonlar uygulanmıştır
# 
# 1-Linklerin temizlenmesi
# 2-Noktalama işaretlerinin temizlenmesi
# 3-Her harfin küçük harf yapılması
# 4-Etkisiz kelimelerin(stopwords) kaldırılması
# 5-Emojilerin kaldırılması
#
# Kullanılan veri setleri Haberler klasörü içerisinde yer almaktadır

import csv
import string
import re

tweets = list()
truetweets = list()

#Her çekilen tweet için dosya yollu düzenlenmelidir
#Konu ile alakalı anahtar kelimelere göre tweetler seçilmektedir
with open('Haberler/tweetler.csv') as truetweet:
    tweets = truetweet.readlines()
    keyword_list = ["corona", "coronavirus", "korona", "koronavirüs", "covid-19", "kovid-19","sağlık bakanı","koronavirüs aşısı"]

    for i in tweets:
        for j in keyword_list:
            if j in i.lower():
                truetweets.append(i)
                break


#Seçilen tweetler içerisinde bulunan linklerin maksimum iki kere yazıldığı göz
#önüne alındığından döngü iki kez tekrarlanmıştır
linksiztweet1=list()
linksiztweet=list()
for tweet in truetweets:
    if "https://t.co/" in tweet:
        baslangicIndex=tweet.index("https://t.co/")
        sonIndex=baslangicIndex+23
        cikarilcakLink=tweet[baslangicIndex:sonIndex]
        tweet=tweet.replace(cikarilcakLink,"")
        linksiztweet1.append(tweet)
    else:
        linksiztweet1.append(tweet)

for tweet in linksiztweet1:
    if "https://t.co/" in tweet:
        baslangicIndex=tweet.index("https://t.co/")
        sonIndex=baslangicIndex+23
        cikarilcakLink=tweet[baslangicIndex:sonIndex]
        tweet=tweet.replace(cikarilcakLink,"")
        linksiztweet.append(tweet)
    else:
        linksiztweet.append(tweet)



#Haberlerde bulunan kelimeler küçük harflere çevrilmesi
#Noktalama işaretleri temizlenmesi
punctuation = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'"]
for i in range(len(linksiztweet)):
    linksiztweet[i]=linksiztweet[i].lower()
    yenitweet = ""
    for j in linksiztweet[i]:
        if j not in punctuation:
            yenitweet += j
    linksiztweet[i]=yenitweet



#Stop words(etkisiz kelimeler) haberlerin içinden çıkartılacak
#Etkisiz kelimelerin listesi Google'un Türkçe için kullandığı kelimelerden oluşmaktadır
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

for i in range(len(linksiztweet)):
    words=linksiztweet[i].split(" ")
    yenitweet = ""
    for j in words:
        if j not in turkçeStopWords:
            yenitweet += j+" "
    linksiztweet[i]=yenitweet


#Tweetlerde bulunan emojilerin temizlenmesi
regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # Genel emoji seti
        u"\U0001F300-\U0001F5FF"  # Semboller
        u"\U0001F680-\U0001F6FF"  # Harita sembolleri
        u"\U0001F1E0-\U0001F1FF"  # Bayrak sembolleri
        u"\U0001F9A0" #Mikrop emojisi
        u"\U0001F498" #Aşı emojisi
        u"\U00002757" #Ünlem emojisi

                           "]+", flags = re.UNICODE)

for i in range(len(linksiztweet)):
    linksiztweet[i]=regrex_pattern.sub(r'',linksiztweet[i])


#Temizlenen tweetlerin ayrılmak için farklı bir dosyaya yazılması
with open('Haberler/truetweetsall2.csv','w') as temizveri:
    for i in range(len(linksiztweet)):
        temizveri.write(linksiztweet[i])
    