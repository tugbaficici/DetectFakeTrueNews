#
# Sınıflandırma Algoritması
# Multinominal Naive Bayes Sınıflandırıcısı
#

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
from cumleTemizleme import cumleTemizle


test1Sonuc=""
test2Sonuc=""
test1Gercek=""
test2Gercek=""

# Performansın hesaplanabilmesi için global olarak tanımlanan test tahmin ve gerçek değerleri kullanılarak
# Doğruluk, kesinlik, anma, f-ölçütü ve karmaşıklık matrisi sınıflandırma sonucunda consolde ve
# pencerelerde gösterilmektedir.
def performans():
    global test1Sonuc,test2Sonuc,test1Gercek,test2Gercek

    print("Doğru-Yalan için")
    print("Doğruluk : ")
    print(accuracy_score(test1Gercek, test1Sonuc))#Doğruluk için
    print("Kesinlik, Anma, F-Ölçütü : ")
    print(classification_report(test1Gercek, test1Sonuc))#Kesinlik, anma ve f-ölçütü için

    print("Bilinçli Yalan-Bilinçsiz Yalan için")
    print("Doğruluk : ")
    print(accuracy_score(test2Gercek, test2Sonuc))#Doğruluk için
    print("Kesinlik, Anma, F-Ölçütü : ")
    print(classification_report(test2Gercek, test2Sonuc))#Kesinlik, anma ve f-ölçütü için

    #Karmaşıklık matrislerinin pencere içine çizilmesi için(hem doğru-yanlış hem de bilinçli-bilinçsiz için)
    label1="Yalan"
    label2="Doğru"
    cm = confusion_matrix(test1Gercek, test1Sonuc)
    fig1=plt.figure(1)
    fig1.suptitle('Doğru-Yalan', fontsize=17)
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=[label1, label2], yticklabels=[label1, label2], cmap=plt.cm.Blues, cbar=False)
    plt.xlabel('Tahmini Sonuç')
    plt.ylabel('Gerçek Sonuç')

    label11="Bilinçsiz Yalan"
    label22="Bilinçli Yalan"
    cm2 = confusion_matrix(test2Gercek, test2Sonuc)
    fig2=plt.figure(2)
    fig2.suptitle('Bilinçli Yalan-Bilinçsiz Yalan', fontsize=17)
    sns.heatmap(cm2, annot=True, fmt='d', xticklabels=[label11, label22], yticklabels=[label11, label22], cmap=plt.cm.Blues, cbar=False)
    plt.xlabel('Tahmini Sonuç')
    plt.ylabel('Gerçek Sonuç')
    plt.show()


# Multinominal Naive Bayes Sınıflandırıcısı fonksiyon tanımı
def naive_bayes(df,testCumlesi,labeltipi):
    # Verilerin uygun hale getirildikten sonra bir diziye atılması
    vectorizer = CountVectorizer()
    veriler= vectorizer.fit_transform(df['title'].values)
    veriler = veriler.toarray()

    # Veri etiketlerinin diziye atılması
    label = df['Label'].values

    # Verinin öğretme ve test olarak ayrılması
    # Burda verinin 3/10'u test olarak, 7/10'u model oluşturulması için kullanılacaktır
    veriler_train, veriler_test, label_train, label_test = train_test_split(veriler, label, shuffle=True, test_size=0.30, random_state=11)

    # Sınıflandırıcının scikit-learn kütüphanesi kullanılarak tanımlanması
    clf = MultinomialNB()

    # Modelin oluşturulması
    clf.fit(veriler_train, label_train)

    # Performansın hesaplanması için test verilerinin tahmini ve gerçek değerleri global değişkene atılmaktadır
    # labeltipi 1 olduğunda doğru-yalan veri için
    # labeltipi 2 olduğunda bilinçli yalan-bilinçsiz yalan ver için kullanılır
    global test1Sonuc,test2Sonuc,test1Gercek,test2Gercek

    if(labeltipi==1):
        test1Gercek=label_test
        test1Sonuc = clf.predict(veriler_test)
    if(labeltipi==2):
        test2Gercek=label_test
        test2Sonuc = clf.predict(veriler_test)
    
    # Tahmin edilecek verinin direk kullanılmadan önce uygun hale getirilmesi için
    vectorized_sentence = vectorizer.transform([testCumlesi]).toarray()
    # Tahminin fonksiyon çıksı olarak geri gönderilmesi
    return clf.predict(vectorized_sentence)


# Cümlenin belirlenmesi
#test = "Merkel koronavirüse yakalandı."
test = "Merkel koronavirüse yakalandı."
# Cümlenin fonksiyona gönderilmeden önce veriseti gibi temizlenmesi
test=cumleTemizle(test)

# İki veriseti kullanılmaktadır
# dogru_yalan= İlk aşamada cümlenin doğruluğu ya da yalanlığı kontrol edilir
# Eğer cümle yalan ise bilincli_bilinsiz veri kullanılarak aynı sınıflandırma tekrarlanır ve sonuç elde edilir.
dogru_yalan = pd.read_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/veri.csv")
bilincli_bilincsiz = pd.read_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/yalanveri.csv")

# Veri etiketleri aşağıdaki gibidir.
# Doğru --> 1
# Yalan --> 0
#       Bilinçli Yalan --> 1
#       Bilinçsiz Yalan --> 0

# İlk aşama fonksiyonu çağırılır
DYSonuc=naive_bayes(dogru_yalan,test,1)
if(DYSonuc==0):# Yalan ise
    BliBsizSonuc=naive_bayes(bilincli_bilincsiz,test,2)
    if(BliBsizSonuc==0):# Bilinçsiz ise
        print("Bilinçsiz Yalan")
        performans() # Performansın hesaplanması için
    else:# Bilinçli ise
        print("Bilinçli Yalan")
        performans() # Performansın hesaplanması için
else:# Doğru ise
    BliBsizSonuc=naive_bayes(bilincli_bilincsiz,test,2)
    print("Doğru")
    performans() # Performansın hesaplanması için