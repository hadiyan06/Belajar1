import tweepy,sys,jsonpickle
import time
import json
 
consumer_key = 'APANIELEdB9eOX4Np68AkuSY7'
consumer_secret = 'ivG58O29iF0eetATQrjPwEHz4rKLu3D8C4Cod5jqtguZ4S8rrG'
 
qry='@sandiuno'
maxTweets = 4000 # Isi sembarang nilai sesuai kebutuhan anda
tweetsPerQry = 100  # Jangan isi lebih dari 100, ndak boleh oleh Twitter
fName=qry+'_'+time.strftime('%Y%m%d-%H%M%S')+'.json' # Nama File hasil Crawling
 
auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    sys.exit('Autentikasi gagal, mohon cek "Consumer Key" & "Consumer Secret" Twitter anda')
 
sinceId=None;max_id=-1;tweetCount=0
print("Mulai mengunduh maksimum {0} tweets".format(maxTweets))
with open(fName,'w') as f:
    f.write("[")
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry)
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1))
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId)
            if not new_tweets:
                print('Tidak ada lagi Tweet ditemukan dengan Query="{0}"'.format(qry))
                break

            if tweetCount > 0:
                f.write(",\n")
            for i,tweet in enumerate(new_tweets):
                data_tweet = dict()
                if i>0:
                    f.write(",\n")
                data_tweet["isi"] = tweet._json["text"]
                data_tweet["tanggal"] = tweet._json["created_at"]
                data_tweet["id_user"] = tweet._json["user"]["id"] 
                data_tweet["akun"] = qry
                data_tweet["sentimen"] = "something"
                f.write(jsonpickle.encode(data_tweet,unpicklable=False))
            tweetCount+=len(new_tweets)
            sys.stdout.write("\r");sys.stdout.write("Jumlah Tweets telah tersimpan: %.0f" %tweetCount);sys.stdout.flush()
            max_id=new_tweets[-1].id
        except tweepy.TweepError as e:
            print("some error : " + str(e));break # Aya error, keluar
    f.write("]")
print ('\nSelesai! {0} tweets tersimpan di "{1}"'.format(tweetCount,fName))