#
# Twitter API kullanılarak tweetlerin kişiye göre ya da hashtage göre çekilmesini sağlar.
# Twitter API kullanılması için Twitter geliştirici hesabına başvurulması 
# ve onaylandıktan sonra proje oluşturulup anahtarların alınması gerekmektedir.
#

from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import pandas as pd
import csv
import string

# Geliştirici hesabından alınan anahtarlar aşağıda verilmiştir
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

# Girilen anahtarların onaylanması
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Tweet çekme işi için fonksiyonun tanımlanması
def tweetCek(kullaniciAdi,arananKelimeler, tarihBaslangici, tweetSayisi):
    # Bir tweet aşağıda tanımlanan özellikleri içermektedir
    db_tweets = pd.DataFrame(columns = ['username', 'acctdesc', 'location', 'following',
                                        'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                        'retweetcount', 'text', 'hashtags'])

    # Tweetler .Cursor() fonksiyonu ile çekilir. 
    # api.user_timeline seçildiğinde kişiye göre arama yapar
    # api.search seçildiğinde verilen hashtaglere göre arama yapılmaktadır
    # Maksimum bir defada 3000 tweet çekilmektedir.
    tweets = tweepy.Cursor(api.user_timeline,id=kullaniciAdi,q=arananKelimeler, lang="tr", since=tarihBaslangici , tweet_mode='extended').items(tweetSayisi)

    # Tweetler sütunları ile bir listede tutulurlar
    tweet_list = [tweet for tweet in tweets]
    noTweets = 0
    for tweet in tweet_list:
        username = tweet.user.screen_name
        acctdesc = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        usercreatedts = tweet.user.created_at
        tweetcreatedts = tweet.created_at
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError: 
            text = tweet.full_text
        ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                     usercreatedts, tweetcreatedts, retweetcount, text, hashtags]
        db_tweets.loc[len(db_tweets)] = ith_tweet
        noTweets += 1

    # Tweetler pandas kütüphanesi ile .csv uzantılı bir dosyaya yazılmaktadırlar
    db_tweets=db_tweets["text"]
    db_tweets.to_csv('/home/tubi/Desktop/DetectFakeTrueNews/Haberler/kisiyegore.csv', index = False)

    print('Çekme tamamlandı!')

# Parametreler belirlenerek fonksiyon çağırılır
aranacakKelimeler = "#kovid-19 OR #covid-19 OR #koronavirüs OR #coronavirus"
tarih = "2019-01-01"
tweetSayisi = 500
kullaniciAdi = 'anadoluajansi'
tweetCek(kullaniciAdi,aranacakKelimeler, tarih, tweetSayisi)