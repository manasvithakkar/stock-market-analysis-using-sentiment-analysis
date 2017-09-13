from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#import MySQLdb
import time
import datetime
import json
import trialmult as p
import pymysql
import filter_data as f
import newdata as n

conn = pymysql.connect(host='localhost', user='root', passwd='', db='twitter')

c = conn.cursor()

#consumer key, consumer secret, access token, access secret.
ckey="W8UfLkSG8Uf0yYf7YjchJcEpb"
csecret="28auybzjuBRf0e1zdhLR5HYucVS0e4mJ4Eih14llS4rvzg9HG3"
atoken="2286274116-ei6sjeI5fpTB4NxjEYUyRdICjgpGROWlp8jnhoR"
asecret="LASavXfE9TUHLGCiAdfROFwL79iVmzdYvRNqnHuOjkMOm"

class listener(StreamListener):

    def on_data(self, data):

        try:
            all_data = json.loads(data)
            
            tweet = all_data["text"]
            filtered = f.filter(tweet)
            filtered = f.tagging(filtered)
            fline = f.remove_stopwords(filtered)
            print(fline)
            print(p.sentiment(fline))
            date = all_data["created_at"]
            datemon= date[4:7]

            datedate= date[8:10]
            dateyear= date[-4:]
           

            if(datemon == "Jan"):
                datemonnew = '01'

            elif(datemon == "Feb"):
                datemonnew = '02'


            elif(datemon == "Mar"):
                datemonnew = '03'

            elif(datemon == 'Apr'):
                datemonnew = '04'

            elif(datemon == 'May'):
                datemonnew = '05'
    
            elif(datemon == 'Jun'):
                datemonnew = '06'

            elif(datemon == 'Jul'):
                datemonnew = '07'

            elif(datemon == 'Aug'):
                datemonnew = '08'

            elif(datemon == 'Sep'):
                datemonnew = '09'

            elif(datemon == 'Oct'):
                datemonnew = '10'

            elif(datemon == 'Nov'):
                datemonnew = '11'

            else:
                datemonnew = '12'


            final = dateyear+ "-" + datemonnew + "-" + datedate
            sentiment_value = p.sentiment(fline)
            print(final,tweet)
            username = all_data["user"]["screen_name"]
            
            c.execute("INSERT INTO sentimenttesting (date, author, tweet, class) VALUES (%s,%s,%s,%s)",
                ( final,username, tweet, sentiment_value))
    
            conn.commit()
                
            return True
        except:
            return True
        
    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(languages=["en"],track=["hdfc,infosys"])