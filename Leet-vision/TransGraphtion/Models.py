from TransGraphtion import db
import pickle

class Accounts(db.Model):
    __tablename__="Accounts"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    username=db.Column(db.Text,unique=True, nullable=False)
    user_dob=db.Column(db.Text)
    aadharid=db.Column(db.Text)
    account_address=db.Column(db.Text)
    socials=db.Column(db.Text)
    userscore=db.Column(db.Text)
    transactions=db.relationship("Transactions",backref="Accounts",primaryjoin="Accounts.id == Transactions.account_id")
    def __init__(self, username,user_dob,aadharid,account_address):
        self.username=username
        self.user_dob=user_dob
        self.aadharid=aadharid
        self.account_address=account_address
        self.userscore="100"
        self.socials=""
    def __repr__(self):
        return f"{self.username}"

class Transactions(db.Model):
    __tablename__="Transactions"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    transactionid=db.Column(db.Text)
    transactiondate=db.Column(db.Text)
    transactiontype=db.Column(db.Text)
    transactionscore=db.Column(db.Text)
    receipentaddress=db.Column(db.Text)
    transactionmedium=db.Column(db.Text)
    transactionamount=db.Column(db.Text)
    transactionbalance=db.Column(db.Text)
    transactiondetails=db.Column(db.Text)
    account_id=db.Column(db.Integer,db.ForeignKey("Accounts.id"))
    def __init__(self, transactionid,transactiondate,transactiontype,receipentaddress, transactionmedium,transactionamount,transactionbalance,transactiondetails,account_id):
        self.transactionid=transactionid
        self.transactiondate=transactiondate
        self.transactiontype=transactiontype
        self.receipentaddress=receipentaddress
        self.transactionmedium=transactionmedium
        self.transactionamount=transactionamount
        self.transactionbalance=transactionbalance
        self.transactiondetails=transactiondetails
        self.account_id=account_id
    def updatescore(self):
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
        self.transactionscore=loaded_model.score([self.transactiontype,self.transactionamount,self.Accounts.account_address,self.receipentaddress])
    def __repr__(self):
        return str({"Date":self.transactiondate,"Type":self.transactiontype,"Receipient":self.receipentaddress})

class UserInteractions(db.Model):
    __tablename__="UserInteractions"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    interactionidid=db.Column(db.Text,unique=True, nullable=False)
    interactiondate=db.Column(db.Text)
    interactionresult=db.Column(db.Text)
    senderaddress=db.Column(db.Text)
    receipentaddress=db.Column(db.Text)
    def __init__(self, interactionidid,interactiondate,senderaddress,receipentaddress,interactionresult):
        self.interactionidid=interactionidid
        self.interactiondate=interactiondate
        self.senderaddress=senderaddress
        self.receipentaddress=receipentaddress
        self.interactionresult=interactionresult
    def __repr__(self):
        return str({"Date":self.interactiondate,"Sender":self.senderaddress,"Receipient":self.receipentaddress})