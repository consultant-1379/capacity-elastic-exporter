import requests
import datetime
from elasticsearch import Elasticsearch


ELASTIC_HOST    =   "192.168.56.109"

#res = requests.get('http://' + ELASTIC_HOST + ':9200')

es = Elasticsearch([{'host': ELASTIC_HOST, 'port': 9200}])





def es_post(payload):
    index = datetime.date.today()
    output =  es.index(
        index=index,
        document=payload
       
    )
    print(output)
    return output


def es_get():
    index = datetime.date.today()
    print(es.get(index=index,id='JXtZCX0BAX8eE9ezVuKl'))
   

