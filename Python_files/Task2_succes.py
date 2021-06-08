from Task1 import openSQLiteFile, reports
import matplotlib.pyplot as plt
import numpy as np
"""
Chargeback'i w zależności od:
- sukcesu
- cb
Wnioski:
- zgłoszenia były tylko w wypadku sukcesu
- zgłoszenia były tylko w wypadku cb = 0
"""

if __name__ == "__main__":
    # -------------
    # Getting data
    # -------------
    cursor = openSQLiteFile("db.sqlite")
    sqlite_data = cursor.execute('\
                SELECT "transactions"."id", "cards"."brand", \
                "transactions"."succes", "transactions"."cb" \
                FROM transactions, cards, customers \
                WHERE "transactions"."card_id" = "cards"."id" \
                AND "transactions"."card_id" = "customers"."card_id"')

    visa_reports = reports("Visa")
    master_reports = reports("Mastercard")


    # -------------
    # Scrappin data
    # -------------
    sqlite_data = [a for a in sqlite_data]
    visa_succes = {"r": 0, "nr": 0}
    mastercard_succes = {"r": 0, "nr": 0}
    visa_cb = {"r": 0, "nr": 0}
    mastercard_cb = {"r": 0, "nr": 0}
    visa_no_succes = {"r": 0, "nr": 0}
    mastercard_no_succes = {"r": 0, "nr": 0}
    visa_no_cb = {"r": 0, "nr": 0}
    mastercard_no_cb = {"r": 0, "nr": 0}

    for data in sqlite_data:
        if data[1] == "visa":
            if data[0] in visa_reports:
                if data[2] == 1:
                    visa_succes["r"] += 1
                else:
                    visa_no_succes["r"] += 1
                if data[3] == 1:
                    visa_cb["r"] += 1
                else:
                    visa_no_cb["r"] += 1
            else:
                if data[2] == 1:
                    visa_succes["nr"] += 1
                else:
                    visa_no_succes["nr"] += 1
                if data[3] == 1:
                    visa_cb["nr"] += 1
                else:
                    visa_no_cb["nr"] += 1
        elif data[1] == "mastercard":
            if data[0] in master_reports:
                if data[2] == 1:
                    mastercard_succes["r"] += 1
                else:
                    mastercard_no_succes["r"] += 1
                if data[3] == 1:
                    mastercard_cb["r"] += 1
                else:
                    mastercard_no_cb["r"] += 1
            else:
                if data[2] == 1:
                    mastercard_succes["nr"] += 1
                else:
                    mastercard_no_succes["nr"] += 1
                if data[3] == 1:
                    mastercard_cb["nr"] += 1
                else:
                    mastercard_no_cb["nr"] += 1


    # -------------
    # Drawing plots
    # -------------
    date_plot = plt.figure(1)
    labels = ["visa succes", "visa no succes", "mastercard succes", "mastercard no succes"]
    
    reported = [visa_succes["r"], visa_no_succes["r"], mastercard_succes["r"], mastercard_no_succes["r"]]
    not_reported = [visa_succes["nr"], visa_no_succes["nr"], mastercard_succes["nr"], mastercard_no_succes["nr"]]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    not_reported_bar = ax.bar(x + width/2, not_reported, width, label="nie zgłoszony")
    reported_bar = ax.bar(x - width/2, reported, width, label="zgłoszony chargeback")

    ax.set_ylabel("Ilość zgłoszeń")
    ax.set_title("Ilość zgłoszeńa a sukces transakcji")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(not_reported_bar, padding=3)
    ax.bar_label(reported_bar, padding=3)
    fig.tight_layout()


    date_plot = plt.figure(2)
    labels = ["visa cb", "visa no cb", "mastercard cb", "mastercard no cb"]
    
    reported = [visa_cb["r"], visa_no_cb["r"], mastercard_cb["r"], mastercard_no_cb["r"]]
    not_reported = [visa_cb["nr"], visa_no_cb["nr"], mastercard_cb["nr"], mastercard_no_cb["nr"]]
    x = np.arange(len(labels))
    width = 0.35



    fig, ax = plt.subplots()
    not_reported_bar = ax.bar(x + width/2, not_reported, width, label="nie zgłoszony")
    reported_bar = ax.bar(x - width/2, reported, width, label="zgłoszony chargeback")

    ax.set_ylabel("Ilość zgłoszeń")
    ax.set_title("Ilość zgłoszeńa a zgłoszenia chargeback'a")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(not_reported_bar, padding=3)
    ax.bar_label(reported_bar, padding=3)
    fig.tight_layout()

    plt.show()
