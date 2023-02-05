from tabula import read_pdf
from tabulate import tabulate

from TransGraphtion.Models import  Accounts, Transactions, UserInteractions
from TransGraphtion import db
import re

#reads table from pdf file
df = read_pdf("./Bank Statements/20189553494.pdf",pages="all") #address of pdf file
print(tabulate(df))

db.create_all()
acct1=Accounts("Sam Christian","1998\01\08","1234 5678 9101","20189553494")
db.session.add(acct1)
db.session.commit()

accs=Accounts.query.all()
account=accs[0]
for account in accs:
    print(account.id)

for page in df:
    page.fillna(0, inplace = True)
    for i, data in page.iterrows():
        if data["Withdrawal"]==0:
            t_type="Deposit"
        else:
            t_type="Withdrawal"
        amount=max(data["Withdrawal"],data["Deposit"])
        if "NEFT" in data["Description"].replace("\r"," "):
            transactiontype="NEFT"
            x = re.findall("TRF FROM [0-9]+",  data["Description"].replace("\r"," "))
            if len(x)>0:
                Receipient=x[0].replace("TRF FROM ","")
        elif "POS ATM" in data["Description"].replace("\r"," "):
            transactiontype="POS Purchase"
            x = re.findall("POS ATM PURCH/[A-Z]*[0-9]+", data["Description"].replace("\r"," "))
            if len(x)>0:
                Receipient=x[0].replace("POS ATM PURCH/","")
        elif "ATM WDL" in data["Description"].replace("\r"," "):
            transactiontype="ATM Withdrawal"
            x = re.findall("ATM WDL /ATM CASH [0-9]+ [A-Z ]+", data["Description"].replace("\r"," "))
            if len(x)>0:
                Receipient=x[0].replace("ATM WDL /ATM CASH ","")
        elif "TRF TO" in data["Description"].replace("\r"," "):
            transactiontype="Bank Transfer"
            x = re.findall("TRF TO [0-9]+",  data["Description"].replace("\r"," "))
            if len(x)>0:
                Receipient=x[0].replace("TRF TO ","")
        elif "CSH DEP" in data["Description"].replace("\r"," "):
            transactiontype="Cash Deposit"
            Receipient="SELF"
        else: 
            transactiontype="Others"
            Receipient=""
        print(transactiontype," \n ",Receipient)
        trans=Transactions(data["BrCd"],data["Date"],transactiontype,Receipient,t_type,amount,data["Balance"],data["Description"],account.id)
        db.session.add(trans)
        db.session.commit()

for i in account.transactions:
    print(i)