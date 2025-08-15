
from tinydb import TinyDB, Query
from datetime import datetime
import os
import subprocess
import random

dir_path = os.path.dirname(os.path.abspath(__file__))
print('path:', dir_path)
db_path = dir_path + '/db/'

class quotesDB:
    def __init__(self, fname = 'activeDB.json'):
        self.activeDB = TinyDB(db_path+fname)

    def insert(self, 
               username="", 
               quote="",
               quoteAuthor="",
               quoteDate="",
               quoteSource=""):
        id = self.activeDB.insert({
            'username': username, 
            'quote': quote, 
            "quoteAuthor": quoteAuthor, 
            "quoteDate": quoteDate,
            "quoteSource": quoteSource,
            'lastUpdateTime':getTimeString(),
            'read':[]
            })
        return id

    def getRandom(self):
        allQuotes = self.activeDB.all()
        all_doc_ids = [doc.doc_id for doc in self.activeDB.all()]
        print(all_doc_ids)
        print()
        random_document = ""
        if all_doc_ids:
            # Randomly select one ID
            random_doc_id = random.choice(all_doc_ids)
            print(f"Randomly selected document ID: {random_doc_id}")

            random_document = self.activeDB.get(doc_id=random_doc_id)
            random_document["id"] = random_doc_id
        #rand_i = random.randint(0, len(allQuotes)-1)
        #return allQuotes[rand_i]
    
        return random_document

    def getQuotes(self, key, value):

        print ("__getQuotes:", key, " : ", value)
        sQuotes = []
        if (key == 'all'):
            quotes = self.activeDB.all()
            for doc in quotes:
                sQuotes.append(doc)
                sQuotes[-1]["id"] = doc.doc_id
            
        return sQuotes
                

    
    def update(self, data):
        
        Line = Query()
        id = self.activeDB.update({
            'username': data['username'], 
            'author': data['author'],
            'date':data['date'],
            'quote':data['quote'],
            'source':data['source']
            }, 
            doc_ids=[data['id']])
        
        return id
    
    def find(self, param="", value=""):
        q = Query()
        result = self.activeDB.search(q[param] == value)
        return result
    
    # def countTier(self, item="", tier="A"):
    #     q = Query()
    #     result = self.activeDB.search((q["item"] == item) & (q["tier"] == tier))
    #     return len(result)
    
    def removeAllEntriesByUser(self, username): #untested
        Line = Query()
        self.activeDB.remove(Line.username == username)

def getTimeString():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def parseTimeString(s):
    return datetime.strptime(s, "%Y/%m/%d %H:%M:%S")



# testing
if __name__ == '__main__':
    db = uDb()
    id = db.insert(ip = '20.0.0.1:80', hostname='makerspace.local', job='Base Station', notes='Base Station')
    id = db.insert(ip = '20.0.0.2:80', hostname='photoResistor.local', job='Makerspace Photoresistor', notes='Photo resistor that monitors light levels in the Makerspace')
    result = db.find('job', "Base Station")
    print(result)