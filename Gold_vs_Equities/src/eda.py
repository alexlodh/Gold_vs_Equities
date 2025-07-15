import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_gold_sp500(csv_path="data/gold_sp500_aligned.csv"):
    """
    Plots gold and S&P 500 prices from a CSV file using matplotlib and seaborn.
    """
    df = pd.read_csv(csv_path, parse_dates=["date"])
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x="date", y="gold", label="Gold")
    sns.lineplot(data=df, x="date", y="sp500", label="S&P 500")
    plt.title("Gold vs S&P 500 Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)/Index value")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_gold_sp500()
