
import csv
import os
from datetime import datetime

FILE_NAME = "loan_records.csv"

# -------------------------------
# APPLICATION DESIGN
# -------------------------------

def welcome():
    print("\n" + "=" * 58)
    print("              SIMPLE LOAN EMI EXPLORER")
    print("             Smart Financial Planning")
    print("=" * 58)
    print("  Calculate | Manage | Analyse | Plan")
    print("=" * 58)


def menu():
    print("\n--------------- MAIN MENU ---------------")
    print("1. Calculate New Loan EMI")
    print("2. View All Loan Records")
    print("3. Search Loan Records")
    print("4. View Financial Summary")
    print("5. Generate EMI Chart")
    print("6. Export Financial Report")
    print("7. Exit")
    print("-----------------------------------------")
    return input("Enter your choice (1-7): ").strip()


# -------------------------------
# INPUT VALIDATION
# -------------------------------

def get_positive_number(message):
    while True:
        try:
            value = float(input(message))

            if value <= 0:
                print("Please enter a value greater than zero.")
                continue

            return value

        except ValueError:
            print("Invalid input! Please enter a number.")


def get_interest_rate():
    while True:
        try:
            rate = float(input("Enter annual interest rate (%): "))

            if rate < 0 or rate > 100:
                print("Interest rate must be between 0 and 100.")
                continue

            return rate

        except ValueError:
            print("Please enter a valid interest rate.")


def get_tenure():
    while True:
        try:
            months = int(input("Enter loan tenure (months): "))

            if months <= 0:
                print("Tenure must be greater than zero.")
                continue

            return months

        except ValueError:
            print("Please enter a valid whole number.")


# -------------------------------
# EMI CALCULATION
# -------------------------------

def calculate_emi(principal, annual_rate, months):

    monthly_rate = annual_rate / (12 * 100)

    if monthly_rate == 0:
        emi = principal / months

    else:
        emi = (
            principal * monthly_rate *
            (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return emi, total_payment, total_interest


# -------------------------------
# CSV DATA MANAGEMENT
# -------------------------------

def initialize_file():

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Loan ID",
                "Customer Name",
                "Loan Amount",
                "Interest Rate",
                "Tenure Months",
                "Monthly EMI",
                "Total Payment",
                "Total Interest",
                "Date"
            ])


def save_record(record):

    initialize_file()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(record)


def read_records():

    initialize_file()

    try:
        with open(FILE_NAME, "r", newline="") as file:
            return list(csv.DictReader(file))

    except (OSError, csv.Error) as error:
        print("Unable to read loan records:", error)
        return []


# -------------------------------
# ADD NEW LOAN
# -------------------------------

def add_loan():

    print("\n========== NEW LOAN ENTRY ==========")

    name = input("Enter customer name: ").strip()

    if not name:
        print("Customer name cannot be empty.")
        return

    amount = get_positive_number("Enter loan amount (Rs.): ")
    rate = get_interest_rate()
    months = get_tenure()

    emi, total, interest = calculate_emi(
        amount, rate, months
    )

    loan_id = "LN" + datetime.now().strftime("%Y%m%d%H%M%S")
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    record = [
        loan_id,
        name,
        round(amount, 2),
        round(rate, 2),
        months,
        round(emi, 2),
        round(total, 2),
        round(interest, 2),
        date
    ]

    save_record(record)

    print("\n" + "=" * 48)
    print("             LOAN SUMMARY")
    print("=" * 48)
    print(f"Customer Name   : {name}")
    print(f"Loan ID         : {loan_id}")
    print(f"Loan Amount     : Rs. {amount:,.2f}")
    print(f"Interest Rate   : {rate:.2f}%")
    print(f"Loan Tenure     : {months} months")
    print("-" * 48)
    print(f"Monthly EMI     : Rs. {emi:,.2f}")
    print(f"Total Payment   : Rs. {total:,.2f}")
    print(f"Total Interest  : Rs. {interest:,.2f}")
    print("=" * 48)
    print("Loan record saved successfully!")


# -------------------------------
# VIEW LOAN RECORDS
# -------------------------------

def view_records():

    records = read_records()

    print("\n========== ALL LOAN RECORDS ==========")

    if not records:
        print("No loan records found.")
        return

    for record in records:
        print("-" * 45)
        print("Loan ID       :", record["Loan ID"])
        print("Customer      :", record["Customer Name"])
        print("Loan Amount   : Rs.", record["Loan Amount"])
        print("Monthly EMI   : Rs.", record["Monthly EMI"])
        print("Total Interest: Rs.", record["Total Interest"])
        print("Date          :", record["Date"])

    print("-" * 45)
    print("Total records:", len(records))


# -------------------------------
# SEARCH LOAN RECORDS
# -------------------------------

def search_records():

    records = read_records()

    keyword = input(
        "\nEnter customer name or Loan ID to search: "
    ).strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    results = [
        record for record in records
        if keyword in record["Customer Name"].lower()
        or keyword in record["Loan ID"].lower()
    ]

    if not results:
        print("No matching loan records found.")
        return

    print("\n========== SEARCH RESULTS ==========")

    for record in results:
        print("-" * 40)
        print("Loan ID:", record["Loan ID"])
        print("Customer:", record["Customer Name"])
        print("Loan Amount: Rs.", record["Loan Amount"])
        print("Monthly EMI: Rs.", record["Monthly EMI"])
        print("Interest: Rs.", record["Total Interest"])


# -------------------------------
# FINANCIAL SUMMARY
# -------------------------------

def financial_summary():

    records = read_records()

    if not records:
        print("\nNo data available for analysis.")
        return

    total_loans = len(records)

    total_amount = sum(
        float(r["Loan Amount"]) for r in records
    )

    total_emi = sum(
        float(r["Monthly EMI"]) for r in records
    )

    total_interest = sum(
        float(r["Total Interest"]) for r in records
    )

    average_emi = total_emi / total_loans

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Loan Records : {total_loans}")
    print(f"Total Loan Amount  : Rs. {total_amount:,.2f}")
    print(f"Combined EMI       : Rs. {total_emi:,.2f}")
    print(f"Total Interest     : Rs. {total_interest:,.2f}")
    print(f"Average EMI        : Rs. {average_emi:,.2f}")
    print("=" * 42)


# -------------------------------
# VISUAL EMI CHART
# -------------------------------

def generate_chart():

    records = read_records()

    if not records:
        print("No records available to generate a chart.")
        return

    try:
        import matplotlib.pyplot as plt

        names = [r["Customer Name"] for r in records]
        emis = [float(r["Monthly EMI"]) for r in records]

        plt.figure(figsize=(10, 5))

        plt.bar(names, emis)

        plt.title("Monthly EMI Comparison")
        plt.xlabel("Customer Names")
        plt.ylabel("Monthly EMI (Rs.)")

        plt.xticks(rotation=35, ha="right")
        plt.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()
        plt.savefig("loan_emi_chart.png")
        plt.show()

        print("Chart saved as loan_emi_chart.png")

    except ImportError:
        print("Matplotlib is not installed.")
        print("Install it using: pip install matplotlib")


# -------------------------------
# EXPORT FINANCIAL REPORT
# -------------------------------

def export_report():

    records = read_records()

    if not records:
        print("No records available to export.")
        return

    try:
        total_amount = sum(
            float(r["Loan Amount"]) for r in records
        )

        total_interest = sum(
            float(r["Total Interest"]) for r in records
        )

        with open("Loan_Financial_Report.md", "w") as file:

            file.write("# SIMPLE LOAN EMI EXPLORER\n\n")
            file.write("## Financial Summary\n\n")
            file.write(f"- Total Records: {len(records)}\n")
            file.write(f"- Total Loan Amount: Rs. {total_amount:,.2f}\n")
            file.write(f"- Total Interest: Rs. {total_interest:,.2f}\n\n")

            file.write("## Loan Details\n\n")

            for r in records:
                file.write(f"### {r['Customer Name']}\n")
                file.write(f"- Loan ID: {r['Loan ID']}\n")
                file.write(f"- Loan Amount: Rs. {r['Loan Amount']}\n")
                file.write(f"- Monthly EMI: Rs. {r['Monthly EMI']}\n")
                file.write(f"- Total Interest: Rs. {r['Total Interest']}\n\n")

        print("\nFinancial report exported successfully!")
        print("File name: Loan_Financial_Report.md")

    except OSError as error:
        print("Report export failed:", error)


# -------------------------------
# MAIN APPLICATION
# -------------------------------

def main():

    initialize_file()
    welcome()

    while True:

        choice = menu()

        if choice == "1":
            add_loan()

        elif choice == "2":
            view_records()

        elif choice == "3":
            search_records()

        elif choice == "4":
            financial_summary()

        elif choice == "5":
            generate_chart()

        elif choice == "6":
            export_report()

        elif choice == "7":
            print("\nThank you for using Simple Loan EMI Explorer!")
            print("Making financial planning simpler.")
            break

        else:
            print("\nInvalid choice! Please select between 1 and 7.")


if __name__ == "__main__":
    main()
