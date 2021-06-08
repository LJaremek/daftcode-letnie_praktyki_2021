from Task1 import openSQLiteFile, reports
import matplotlib.pyplot as plt
import datetime
"""
Chargeback'i na przestrzeni czasu.
Wykresy z:
- całego okresu czasu
- dni tygodnia
- godzin doby
Wnioski:
- minimalne wachania na przestrzeni całego czasu
- brak zauważalnych zmian na przestrzeni tygodnia / dnia
"""

if __name__ == "__main__":
    # -------------
    # Getting data
    # -------------
    cursor = openSQLiteFile("db.sqlite")
    sqlite_data = cursor.execute('\
                SELECT "transactions"."id", "transactions"."created_at" \
                FROM transactions, cards, customers \
                WHERE "transactions"."card_id" = "cards"."id" \
                AND "transactions"."card_id" = "customers"."card_id"')

    visa_reports = reports("Visa")
    master_reports = reports("Mastercard")


    # -------------
    # Scrappin data
    # -------------
    sqlite_data = [a for a in sqlite_data]
    date_nr = {}
    time_nr = {}
    days_nr = {}
    date_r = {}
    time_r = {}
    days_r = {}
    x_axcis = []
    for data in sqlite_data:
        x_axcis.append(data[1][:7])
        if data[0] in visa_reports or data[0] in master_reports:
            try:
                date_r[data[1][:10]] += 1
            except KeyError:
                date_r[data[1][:10]] = 1
            try:
                time_r[data[1][11:13]] += 1
            except KeyError:
                time_r[data[1][11:13]] = 1
            try:
                date = datetime.datetime.strptime(data[1][:10], "%Y-%m-%d")
                day = date.strftime('%A')
                days_r[day] += 1
            except KeyError:
                days_r[day] = 1
        else:
            try:
                date_nr[data[1][:10]] += 1
            except KeyError:
                date_nr[data[1][:10]] = 1
            try:
                time_nr[data[1][11:13]] += 1
            except KeyError:
                time_nr[data[1][11:13]] = 1
            try:
                date = datetime.datetime.strptime(data[1][:10], "%Y-%m-%d")
                day = date.strftime('%A')
                days_nr[day] += 1
            except KeyError:
                days_nr[day] = 1


    # -------------
    # Drawing plots
    # -------------
    x_axcis = list(set(x_axcis))

    date_plot = plt.figure(1)
    fig, ax = plt.subplots()
    plt.title("Zgłoszenia chagebacków na sprzetrzeni czasu")
    plt.xlabel("Data")
    plt.ylabel("Ilość zgłoszeń")

    lists = sorted(date_nr.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Nie głoszone chargeback'i")

    lists = sorted(date_r.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Zgłoszone chargeback'i")

    plt.legend()
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))



    time_plot = plt.figure(2)
    fig, ax = plt.subplots()
    plt.title("Zgłoszenia chagebacków na sprzetrzeni dnia")
    plt.xlabel("Godzina")
    plt.ylabel("Ilość zgłoszeń")

    lists = sorted(time_nr.items())
    x, y = zip(*lists)
    plt.plot(x, y, label= "Nie głoszone chargeback'i")

    lists = sorted(time_r.items())
    x, y = zip(*lists)
    plt.plot(x, y, label= "Zgłoszone chargeback'i")

    plt.legend()



    days_plot = plt.figure(3)
    fig, ax = plt.subplots()
    plt.title("Zgłoszenia chagebacków na sprzetrzeni tygodnia")
    plt.xlabel("Dzień tygodnia")
    plt.ylabel("Ilość zgłoszeń")

    lists = sorted(days_nr.items())
    x, y = zip(*lists)
    plt.plot(x, y, label= "Nie zgłoszone chargeback'i")

    lists = sorted(days_r.items())
    x, y = zip(*lists)
    plt.plot(x, y, label= "Zgłoszone chargeback'i")

    plt.legend()
    plt.show()
