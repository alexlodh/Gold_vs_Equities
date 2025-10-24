import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_gold_sp500(csv_path):
    """
    Plots gold and S&P 500 prices from a CSV file using matplotlib and seaborn.

    Args:
        csv_path (str): Path to the CSV file containing gold and S&P 500 data.
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

from utils.load_config import load_config

if __name__ == "__main__":
    config = load_config("config.yaml")
    csv_path = config.get("csv_path", "../data/gold_sp500_aligned.csv")
    plot_gold_sp500(csv_path)
