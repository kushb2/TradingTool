from app.services.stock_data_service import StockDataService
from app.managers.stock_analysis_manager import StockAnalysisManager
from app.common.constants import CONSOLE_TICKERS


def main():
    print("\n" + "=" * 95)
    print(f"{'STOCK':<15} {'LTP':<10} {'RSI SIGNAL':<25} {'RSI':<10} {'50DMA':<10} {'52W HIGH':<12} {'EARNINGS'}")
    print("=" * 95)

    tickers = CONSOLE_TICKERS

    stock_data_service = StockDataService()
    stock_analysis_manager = StockAnalysisManager()

    processed_stocks = []

    for ticker in tickers:
        stock_data = stock_data_service.fetch_history(ticker)
        
        if not stock_data:
            print(f"Warning: No data found for {ticker}")
            continue

        stock = stock_analysis_manager.calculate_metrics(ticker, stock_data)
        processed_stocks.append(stock)

        stats = stock.analysis

        if stats:
            earnings = stats.get('Earnings_Date', 'N/A')
            if hasattr(earnings, 'date'):
                earnings = earnings.date()

            rsi_signal = stats.get('RSI_Signal', 'N/A')
            rsi_value = stats.get('RSI', 'N/A')

            print(
                f"{ticker:<15} {stats.get('LTP', 'N/A'):<10} {rsi_signal:<25} {rsi_value:<10} {stats.get('50_Day_MA', 'N/A'):<10} {stats.get('52_Week_High', 'N/A'):<12} {earnings}")

    print("=" * 95 + "\n")

    print("\n" + "=" * 40)
    print("Raw RSI Data (Last 5 Days)")
    print("=" * 40)
    for stock in processed_stocks:
        if stock.rsi_series is not None and not stock.rsi_series.empty:
            print(f"\n--- {stock.ticker} ---")
            rsi_history = stock.rsi_series.tail(5)
            for date, rsi_val in rsi_history.items():
                print(f"  {date.strftime('%Y-%m-%d')}: {rsi_val:.2f}")
    print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
