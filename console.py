from app.services.stock_data_service import StockDataService
from app.managers.stock_analysis_manager import StockAnalysisManager
from app.common.constants import CONSOLE_TICKERS
from app.helpers.rsi_helper import get_rsi_description


def main():
    print("\n" + "=" * 85)
    print(f"{'STOCK':<15} {'LTP':<10} {'RSI':<20} {'50DMA':<10} {'52W HIGH':<12} {'EARNINGS'}")
    print("=" * 85)

    # You can add as many stocks as you want here
    tickers = CONSOLE_TICKERS

    stock_data_service = StockDataService()
    stock_analysis_manager = StockAnalysisManager()

    for ticker in tickers:
        stock_data = stock_data_service.fetch_history(ticker)
        
        if not stock_data:
            print(f"Warning: No data found for {ticker}")
            continue

        stock = stock_analysis_manager.calculate_metrics(ticker, stock_data)

        stats = stock.analysis

        if stats:
            # We use 'get' to safely retrieve the date, defaulting to N/A if missing
            earnings = stats.get('Earnings_Date', 'N/A')

            # If earnings is a datetime object, format it nicely (YYYY-MM-DD)
            if hasattr(earnings, 'date'):
                earnings = earnings.date()

            rsi_value = stats['RSI']
            rsi_description = get_rsi_description(rsi_value)
            rsi_display = f"{rsi_value} ({rsi_description})"

            print(
                f"{ticker:<15} {stats['LTP']:<10} {rsi_display:<20} {stats['50_Day_MA']:<10} {stats['52_Week_High']:<12} {earnings}")

    print("=" * 85 + "\n")


if __name__ == "__main__":
    main()
