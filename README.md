# **Daftcode</br>Rekrutacja na letnie praktyki 2021**
</br>

## Intro</br>
Chargebacks are one of the major threats that online merchants have to deal with. To find out
what they are and how they affect business, please look below.</br>
</br>
Chargeback is the return of funds to a consumer, initiated by the issuing bank of the instrument
used by a consumer to settle a debt. Specifically, it is the reversal of a prior outbound transfer of
funds from a consumer's bank account, line of credit, or credit card.
Chargebacks also occur in the distribution industry. This type of chargeback occurs when the
supplier sells a product at a higher price to the distributor than the price they have set with the
end user. The distributor then submits a chargeback to the supplier so they can recover the
money lost in the transaction.</br>
More [https://en.wikipedia.org/wiki/Chargeback]</br>
</br>
AND</br>
</br>
What is a chargeback? In simple terms, it's the reversal of a credit card payment that comes
directly from the bank.</br>
If you're a merchant, chargebacks can be a frustrating threat to your livelihood. If you're a
consumer, chargebacks represent a shield between you and dishonest merchants. If those two
things seem at odds, well, that was never the way it was intended.
To understand how chargebacks work (and how they don't), it helps to have some background
on the rationale behind chargebacks, and the impact they have on those involved.
More [https://chargebacks911.com/chargebacks/]</br>
</br></br>

## Tasks</br>

### **Task 1**</br>
Write a script in python to match reported chargebacks (excel file) with transactions from the
database.</br>

### **Task 2**</br>
Conduct analysis to find sources of chargebacks.</br>

### **Task 3**</br>
The critical chargeback level for merchants is 1%. Based on conducted analysis, please
propose actions aimed at reducing the merchant’s chargeback rate to less than 1%. Please,
submit your solution as a presentation in PDF or pptx.</br>
</br></br>

## Database schema description</br>

### **Table Cards:**</br>
● Id: card id</br>
● Created_at: date and time when card was created</br>
● bin : first 6 digits from card number</br>
● Last_4: last 4 digits from card number</br>
● Brand: card brand</br>
● Bin_country: country code where card issuer is registered</br>
</br>

### **Tabel Customers:**</br>
● Id: customer id</br>
● Created_at: date and time when customer was created</br>
● Card_id: customers card id</br>
● Name: customer name</br>
● Email: customers email</br>
● Ip_addr: customers ip address</br>
</br>

### **Table Transactions:**</br>
● Id: transaction id</br>
● Created_at: date and time when transaction was created</br>
● succes: binary indicator whether transaction was successfully processed</br>
● amount: transaction amount in minor units</br>
● currency: transaction currency</br>
● acq_tid: external transaction id</br>
● card_id: card on which transaction was made</br>
● cb: binary indicator whether transaction has reported chargeback</br>
