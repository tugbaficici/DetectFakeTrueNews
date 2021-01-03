#
# Verilerin temizleme sonrasında istenilen etiketlerin eklenmesi için oluşturulmuştur.
# pandas kütüphanesi .csv uzantılı dosyaların okunup işlenmesini sağlamaktadır.
#
import pandas as pd

# Dosya okunarak "Label" etiketi eklenir ve,
# Doğru tweetler için 1
# Yalan tweetler için 0
# Bilinçli Yalan tweetler için 1
# Bilinçsiz Yalan tweetler için 0 etiketlemesi yapılmıştır.
#
# Her etiketleme işlemi için dosya yolları düzeltilerek kullanılmıştır.
df=pd.read_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/LabelsizVeri/dogru.csv")
df["Label"]=1
df.to_csv("/home/tubi/Desktop/DetectFakeTrueNews/KullanilacakVeriler/LabelliVeri/dogru1.csv",index=False)