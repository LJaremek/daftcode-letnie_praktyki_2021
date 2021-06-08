from Task1 import openSQLiteFile, reports
from matplotlib import pyplot as plt



# -------------
# Getting data
# -------------
reported_id = reports("Visa") + reports("Mastercard")

cursor = openSQLiteFile("db.sqlite")
# sqlite_data = cursor.execute('\
#             SELECT "transactions"."id", "transactions"."created_at" \
#             FROM transactions')
sqlite_data = cursor.execute(f'SELECT "transactions"."id", \
    "transactions"."created_at" \
    FROM transactions, customers, cards \
    WHERE "transactions"."card_id" = "cards"."id" \
    AND "customers"."card_id" = "cards"."id" \
    AND "customers"."ip_country" == "cards"."bin_country"')



# -------------
# Scrappin data
# -------------
reported_data = {}
not_reported_data = {}

for data in sqlite_data:
    trans_id = data[0]
    if trans_id in reported_id:
        try:
            reported_data[data[1][:7]] += 1
        except KeyError:
            reported_data[data[1][:7]] = 1
    else:
        try:
            not_reported_data[data[1][:7]] += 1
        except KeyError:
            not_reported_data[data[1][:7]] = 1

reported_data.update(dict((date, 0) for date in not_reported_data.keys() if date not in reported_data.keys()))
not_reported_data.update(dict((date, 0) for date in reported_data.keys() if date not in not_reported_data.keys()))
chargebacks_lvl = {}

for key, value in reported_data.items():
    chargebacks_lvl[key] = (value / (not_reported_data[key] + value))*100



# -------------
# Drawing plots
# -------------
fig, ax = plt.subplots()
ax.bar(range(len(list(chargebacks_lvl.keys()))), list(chargebacks_lvl.values()))
ax.set_xticklabels(chargebacks_lvl.keys())
ax.set_xticks(range(len(list(chargebacks_lvl.keys()))))
plt.axhline(y=1, color='red', linestyle='--')
ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_ylabel("Poziom obciążeń zwrotnych [%]")
ax.set_xlabel("Data [YYYY-MM]")
# ax.set_title("Poziom obciążeń zwrotnych na przestrzeni czasu")
ax.set_title("Poziom obciążeń zwrotnych na przestrzeni czasu 2")

plt.show()
