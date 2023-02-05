from TransGraphtion import app,db,redirect,url_for
from TransGraphtion.Models import Accounts,Transactions,UserInteractions
import requests
from flask import render_template
from sklearn.naive_bayes import GaussianNB
import pickle
@app.route("/")
def home():
    return """Status : Up"""

@app.route("/train")
async def trainmodel():
    data=UserInteractions.query.all()
    cleaneddata=[[x.interactionidid, x.interactiondate,x.senderaddress,x.receipentaddress ] for x in  data]
    confirmedresults=[x.interactionresult]
    NBclassifier = GaussianNB()
    NBmodel = await NBclassifier.fit(cleaneddata, confirmedresults)
    filename = 'finalized_model.sav'
    pickle.dump(NBmodel, open(filename, 'wb'))    
    
if __name__=="__main__":
    db.create_all()
    app.run(threaded=True)  