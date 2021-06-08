from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from Task1 import openSQLiteFile, reports

# -------------
# Getting data
# -------------
reported_id = reports("Visa") + reports("Mastercard")

cursor = openSQLiteFile("db.sqlite")
sqlite_data = cursor.execute(f'SELECT "transactions"."id", \
    "cards"."created_at", \
    "cards"."exp_year", "cards"."exp_month", "cards"."brand", \
    "cards"."bin", "cards"."last_4", "cards"."bin_country", \
    "customers"."created_at", \
    "customers"."name", "customers"."email", \
    "customers"."ip_addr", "customers"."ip_country", \
    "transactions"."created_at", \
    "transactions"."succes", "transactions"."amount", \
    "transactions"."currency", "transactions"."acq_tid", \
    "transactions"."cb" \
    FROM transactions, customers, cards \
    WHERE "transactions"."card_id" = "cards"."id" \
    AND "customers"."card_id" = "cards"."id" \
    AND "customers"."ip_country" == "cards"."bin_country"')


# -------------
# Scrappin data
# -------------
sqlite_data = [row for row in sqlite_data]
for index, row in enumerate(sqlite_data):
    row = list(row)
    id = row.pop(0)
    if id in reported_id:
        row.append(1)
    else:
        row.append(0)
    sqlite_data[index] = row


ca_created = [row[0] for row in sqlite_data]
ca_year = [row[1] for row in sqlite_data]
ca_month = [row[2] for row in sqlite_data]
ca_brand = [row[3] for row in sqlite_data]
ca_bin = [row[4] for row in sqlite_data]
ca_last = [row[5] for row in sqlite_data]
ca_country = [row[6] for row in sqlite_data]

cu_created = [row[7] for row in sqlite_data]
cu_name = [row[8] for row in sqlite_data]
cu_email = [row[9] for row in sqlite_data]
cu_addr = [row[10] for row in sqlite_data]
cu_country = [row[11] for row in sqlite_data]

tr_created = [row[12] for row in sqlite_data]
tr_succes = [row[13] for row in sqlite_data]
tr_amount = [row[14] for row in sqlite_data]
tr_currency = [row[15] for row in sqlite_data]
tr_acq = [row[16] for row in sqlite_data]
tr_cb = [row[17] for row in sqlite_data]

reported = [row[18] for row in sqlite_data]


pd_frame = pd.DataFrame({"ca_created": ca_created,
                        "ca_year": ca_year,
                        "ca_month": ca_month,
                        "ca_brand": ca_brand,
                        "ca_bin": ca_bin,
                        "ca_last": ca_last,
                        "ca_country": ca_country,

                        "cu_created": cu_created,
                        "cu_name": cu_name,
                        "cu_email": cu_email,
                        "cu_addr": cu_addr,
                        "cu_country": cu_country,

                        "tr_created": tr_created,
                        "tr_succes": tr_succes,
                        "tr_amount": tr_amount,
                        "tr_currency": tr_currency,
                        "tr_acq": tr_acq,
                        "tr_cb": tr_cb,
                        
                        "reported": reported})


pd_frame["ca_created"], ca_created_codes = pd.factorize(pd_frame["ca_created"])
pd_frame["ca_year"], ca_year_codes = pd.factorize(pd_frame["ca_year"])
pd_frame["ca_month"], ca_month_codes = pd.factorize(pd_frame["ca_month"])
pd_frame["ca_brand"], ca_brand_codes = pd.factorize(pd_frame["ca_brand"])
pd_frame["ca_bin"], ca_bin_codes = pd.factorize(pd_frame["ca_bin"])
pd_frame["ca_last"], ca_last_codes = pd.factorize(pd_frame["ca_last"])
pd_frame["ca_country"], ca_country_codes = pd.factorize(pd_frame["ca_country"])

pd_frame["cu_created"], cu_created_codes = pd.factorize(pd_frame["cu_created"])
pd_frame["cu_name"], cu_name_codes = pd.factorize(pd_frame["cu_name"])
pd_frame["cu_email"], cu_email_codes = pd.factorize(pd_frame["cu_email"])
pd_frame["cu_addr"], cu_addr_codes = pd.factorize(pd_frame["cu_addr"])
pd_frame["cu_country"], cu_country_codes = pd.factorize(pd_frame["cu_country"])

pd_frame["tr_created"], tr_created_codes = pd.factorize(pd_frame["tr_created"])
pd_frame["tr_succes"], tr_succes_codes = pd.factorize(pd_frame["tr_succes"])
pd_frame["tr_amount"], tr_amount_codes = pd.factorize(pd_frame["tr_amount"])
pd_frame["tr_currency"], tr_currency_codes = pd.factorize(pd_frame["tr_currency"])
pd_frame["tr_acq"], tr_acq_codes = pd.factorize(pd_frame["tr_acq"])
pd_frame["tr_cb"], tr_cb_codes = pd.factorize(pd_frame["tr_cb"])

pd_frame["reported"], reported_codes = pd.factorize(pd_frame["reported"])


# -----------------------
# Using linear regression
# -----------------------
X = pd_frame.drop(["reported"], axis= 1)
y = pd_frame["reported"]


classifier = LinearRegression()
classifier.fit(X= X, y= y)


importance = classifier.coef_
labels = list(pd_frame.columns)


# -------------
# Drawing plots
# -------------
fig, ax = plt.subplots()
plt.bar([x for x in range(len(importance))], importance)
ax.set_xticklabels(labels)
ax.set_xticks(np.arange(len(labels)))
ax.set_xlabel("Parametry")
ax.set_ylabel("Istotność parametrów")
ax.set_title("Regresja liniowa po wykluczeniu osób wykonujących przelew z innego kraju")
plt.show()
