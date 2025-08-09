import yfinance as shanfinance
import csv
import os

# 📥 Get stock price from GOOGLE Finance
def get_stock_price(ticker):
    try:
        stock = shanfinance.Ticker(ticker)
        data = stock.history(period="1d")
        return data['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return 0.0

# 💰 Calculate total portfolio value
def calculate_portfolio_value(portfolio):
    total = 0
    details = []
    for ticker, shares in portfolio.items():
        price = get_stock_price(ticker)
        value = price * shares
        details.append((ticker.upper(), shares, round(price, 2), round(value, 2)))
        total += value
    return total, details

# 📤 Save to TXT
def save_to_txt(details, total_value, filename="portfolio_value.txt"):
    with open(filename, "w") as file:
        for ticker, shares, price, value in details:
            file.write(f"{ticker}: {shares} shares × ${price:.2f} = ${value:.2f}\n")
        file.write(f"\nTotal Portfolio Value: ${total_value:.2f}\n")

# 📄 Save to CSV
def save_to_csv(details, total_value, filename="portfolio_value.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ticker", "Shares", "Price", "Value"])
        for row in details:
            writer.writerow(row)
        writer.writerow([])
        writer.writerow(["Total Portfolio Value", "", "", f"${total_value:.2f}"])

#User input
def get_user_portfolio():
    portfolio = {}
    print("Enter stock tickers and number of shares (type 'done' to finish):")
    while True:
        ticker = input("Ticker: ").strip()
        # TICKER : AAPL -180 shares
        # TICKER : TSLA -250 shares
        # YOU CAN ADD MORE TICKER WITH SHARES .AFTER, WRITE DONE

        if ticker.lower() == "done":
            break
        try:
            shares = int(input(f"Shares of {ticker}: "))
            portfolio[ticker.upper()] = shares
        except ValueError:
            print("Please enter a valid number.")
    return portfolio

# Main execution
if __name__ == "__main__":
    portfolio = get_user_portfolio()
    if portfolio:
        total_value, details = calculate_portfolio_value(portfolio)
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        save_to_txt(details, total_value)
        save_to_csv(details, total_value)
        print("\nSaved to portfolio_value.txt and portfolio_value.csv")
        print("Location:", os.getcwd())
    else:
        print("No stocks entered.")