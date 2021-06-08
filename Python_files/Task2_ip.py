from Task1 import openSQLiteFile, reports
import matplotlib.pyplot as plt
import numpy as np
"""
Chargeback'i w zależności od:
- rodzaju adresu IP
Wnioski:
- zdecydowana większość klientów dokonywała zgłoszeń z adresu ipv4
"""

if __name__ == "__main__":
    # -------------
    # Getting data
    # -------------
    cursor = openSQLiteFile("db.sqlite")
    sqlite_data = cursor.execute('\
                SELECT "transactions"."id", "cards"."brand", \
                "customers"."ip_addr" \
                FROM transactions, cards, customers \
                WHERE "transactions"."card_id" = "cards"."id" \
                AND "transactions"."card_id" = "customers"."card_id"')

    visa_reports = reports("Visa")
    master_reports = reports("Mastercard")


    # -------------
    # Scrappin data
    # -------------
    sqlite_data = [a for a in sqlite_data]
    visa_ipv4 = {"nr": 0, "r": 0}
    visa_ipv6 = {"nr": 0, "r": 0}
    master_ipv4 = {"nr": 0, "r": 0}
    master_ipv6 = {"nr": 0, "r": 0}
    for data in sqlite_data:
        if data[1] == "visa":
            if data[0] in visa_reports:
                if ":" in data[2]:
                    visa_ipv6["r"] += 1
                else:
                    visa_ipv4["r"] += 1
            else:
                if ":" in data[2]:
                    visa_ipv6["nr"] += 1
                else:
                    visa_ipv4["nr"] += 1
        elif data[1] == "mastercard":
            if data[0] in master_reports:
                if ":" in data[2]:
                    master_ipv6["r"] += 1
                else:
                    master_ipv4["r"] += 1
            else:
                if ":" in data[2]:
                    master_ipv6["nr"] += 1
                else:
                    master_ipv4["nr"] += 1


    # -------------
    # Drawing plots
    # -------------        
    labels = ["visa ipv4", "visa ipv6", "mastercard ipv4", "mastercard ipv6"]
    
    reported = [visa_ipv4["r"], visa_ipv6["r"], master_ipv4["r"], master_ipv6["r"]]
    not_reported = [visa_ipv4["nr"], visa_ipv6["nr"], master_ipv4["nr"], master_ipv6["nr"]]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    not_reported_bar = ax.bar(x + width/2, not_reported, width, label= "nie zgłoszony")
    reported_bar = ax.bar(x - width/2, reported, width, label= "zgłoszony chargeback")

    ax.set_ylabel("Ilość zgłoszeń")
    ax.set_title("Ilość zgłoszeń a adres IPV")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(not_reported_bar, padding= 3)
    ax.bar_label(reported_bar, padding= 3)

    fig.tight_layout()


    plt.show()
