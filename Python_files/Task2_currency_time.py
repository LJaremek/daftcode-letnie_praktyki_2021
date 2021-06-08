from matplotlib import pyplot as plt


from Task1 import openSQLiteFile, reports


# -------------
# Getting data
# -------------
reported_id = reports("Visa") + reports("Mastercard")


cursor = openSQLiteFile("db.sqlite")
sqlite_data = cursor.execute(f'SELECT "transactions"."id", \
    "transactions"."currency", "cards"."created_at"    \
    FROM transactions, customers, cards \
    WHERE "transactions"."card_id" = "cards"."id" \
    AND "customers"."card_id" = "cards"."id" \
    AND "customers"."ip_country" == "cards"."bin_country"')


# -------------
# Scrappin data
# -------------
sqlite_data = [row for row in sqlite_data]
reported_USD = {}
reported_EUR = {}
not_reported_USD = {}
not_reported_EUR = {}
for index, row in enumerate(sqlite_data):
    row = list(row)
    id = row.pop(0)
    curr = row.pop(0)
    time = row.pop(0)[:7]
    if id in reported_id:
        try:
            if curr == "USD":
                reported_USD[time] += 1
            else:
                reported_EUR[time] += 1
        except KeyError:
            if curr == "USD":
                reported_USD[time] = 1
            else:
                reported_EUR[time] = 1
    else:
        try:
            if curr == "USD":
                not_reported_USD[time] += 1
            else:
                not_reported_EUR[time] += 1
        except KeyError:
            if curr == "USD":
                not_reported_USD[time] = 1
            else:
                not_reported_EUR[time] = 1


# -------------
# Drawing plots
# -------------
plt.title("Utworzenia kont z których zgłoszono chargeback'i w czasie")
plt.xlabel("Data")
plt.ylabel("Ilość zgłoszeń")

x1, y1 = zip(*sorted(reported_USD.items()))
plt.plot(x1, y1, label= "Zgłoszone chargeback'i w Dolarach")

x2, y2 = zip(*sorted(reported_EUR.items()))
plt.plot(x2, y2, label= "Zgłoszone chargeback'i w Euro")

y3 = [y1[i] + y2[i] for i, y in enumerate(y1)]
plt.plot(x2, y3, label= "Zgłoszone chargeback'i w Euro i Dolarach")

plt.legend()
plt.show()
