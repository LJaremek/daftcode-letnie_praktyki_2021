from Task1 import openSQLiteFile, reports
import matplotlib.pyplot as plt
import numpy as np
"""
Chargeback'i w zależności od:
- kraju z którego wykonano przelew
- kraju pochodzenia klienta
- różnicy kraju pochodzenia klienta i wykonania przelewu
Wnioski:
- wyraźne skoki wykonane w krajach: PA, RU, TR, TH
- wyraźne skoki u klientów z krajów: US, RU, TR, TH
- większość klientów zlecała przelew z tego samego kraju,
  natomiast gdy przelew pochodził z innego kraju
  większość zleceń została głoszona (~2/3)
"""

if __name__ == "__main__":
    # -------------
    # Getting data
    # -------------
    cursor = openSQLiteFile("db.sqlite")
    sqlite_data = cursor.execute('\
                SELECT "transactions"."id", "cards"."bin_country", \
                "customers"."ip_country" \
                FROM transactions, cards, customers \
                WHERE "transactions"."card_id" = "cards"."id" \
                AND "transactions"."card_id" = "customers"."card_id"')

    visa_reports = reports("Visa")
    master_reports = reports("Mastercard")


    # -------------
    # Scrappin data
    # -------------
    sqlite_data = [a for a in sqlite_data]
    bin_country_nr = {}
    bin_country_r = {}
    ip_country_nr = {}
    ip_country_r = {}
    another_country = {"nr": 0, "r": 0}
    the_same_country = {"nr": 0, "r": 0}

    for data in sqlite_data:
        if data[0] in visa_reports or data[0] in master_reports:
            if data[1] != data[2]:
                try:
                    another_country["r"] += 1
                except KeyError:
                    another_country["r"] = 1
            else:
                try:
                    the_same_country["r"] += 1
                except KeyError:
                    the_same_country["r"] = 1
            try:
                bin_country_r[data[1]] += 1
            except KeyError:
                bin_country_r[data[1]] = 1
            try:
                ip_country_r[data[2]] += 1
            except KeyError:
                ip_country_r[data[2]] = 1
        else:
            if data[1] != data[2]:
                try:
                    another_country["nr"] += 1
                except KeyError:
                    another_country["nr"] = 1
            else:
                try:
                    the_same_country["nr"] += 1
                except KeyError:
                    the_same_country["nr"] = 1
            try:
                bin_country_nr[data[1]] += 1
            except KeyError:
                bin_country_nr[data[1]] = 1
            try:
                ip_country_nr[data[2]] += 1
            except KeyError:
                ip_country_nr[data[2]] = 1
    

    # -------------
    # Drawing plots
    # -------------
    date_plot = plt.figure(1)
    fig, ax = plt.subplots()
    plt.title("Zgłoszone chargebacki w zależności od kraju pochodzenia klienta")
    plt.xlabel("Kraj pochodzenia klienta")
    plt.ylabel("Ilość zgłoszeń")

    lists = sorted(bin_country_nr.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Nie głoszone chargeback'i")

    lists = sorted(bin_country_r.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Zgłoszone chargeback'i")

    plt.legend()



    date_plot = plt.figure(2)
    fig, ax = plt.subplots()
    plt.title("Zgłoszone chargebacki w zależności od kraju wykonania transakcji")
    plt.xlabel("Kraj wykonania transakcji")
    plt.ylabel("Ilość zgłoszeń")

    lists = sorted(ip_country_nr.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Nie głoszone chargeback'i")

    lists = sorted(ip_country_r.items())
    x, y = zip(*lists)
    plt.plot(x, y, label="Zgłoszone chargeback'i")

    plt.legend()



    date_plot = plt.figure(3)
    labels = ["Inny kraj", "Ten sam kraj"]
    
    reported = [another_country["r"], the_same_country["r"]]
    not_reported = [another_country["nr"], the_same_country["nr"]]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    not_reported_bar = ax.bar(x + width/2, not_reported, width, label="nie zgłoszony")
    reported_bar = ax.bar(x - width/2, reported, width, label="zgłoszony chargeback")

    ax.set_ylabel("Ilość zgłoszeń")
    ax.set_title("Transakcje w zależności od różnicy kraju pochodzenia klienta a wysłanego przelewu")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(not_reported_bar, padding=3)
    ax.bar_label(reported_bar, padding=3)

    fig.tight_layout()


    plt.show()
