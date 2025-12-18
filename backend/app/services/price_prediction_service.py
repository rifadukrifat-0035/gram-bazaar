# backend/app/services/price_prediction_service.py
import random
from typing import List, Dict
from datetime import datetime, timedelta

class PricePredictionService:
    """
    A mock price prediction service that simulates an LSTM model
    by generating plausible random data and strategic advice.
    """
    def generate_mock_forecast(self, base_price: float) -> List[Dict]:
        """Generates a list of mock daily price points for the next 7 days."""
        forecast = []
        current_price = base_price
        trend = random.choice([-1, 1]) # -1 for falling, 1 for rising

        for i in range(7):
            date_str = (datetime.now() + timedelta(days=i)).strftime('%d-%b')
            # Add more volatility at the beginning and less towards the end
            volatility = random.uniform(0.98, 1.03)
            current_price = current_price * volatility + (i * trend * 0.2)
            forecast.append({"date": date_str, "price": round(current_price, 2)})
        return forecast

    def get_ai_advice(self, forecast_data: List[Dict]) -> str:
        """Generates simple, actionable advice based on the trend."""
        start_price = forecast_data[0]['price']
        end_price = forecast_data[-1]['price']
        peak_price = max(d['price'] for d in forecast_data)

        if peak_price > start_price * 1.05:
            return f"দাম বাড়ার সম্ভাবনা আছে। সর্বোচ্চ দাম {peak_price} টাকা পর্যন্ত হতে পারে। ২-৩ দিন অপেক্ষা করতে পারেন।"
        elif end_price < start_price * 0.95:
            return "দাম কমার দিকে। লোকসান এড়াতে দ্রুত বিক্রি করার কথা ভাবতে পারেন।"
        else:
            return "বাজার স্থিতিশীল মনে হচ্ছে। বর্তমান দামে বিক্রি করা একটি ভালো সিদ্ধান্ত হতে পারে।"

price_prediction_service = PricePredictionService()
