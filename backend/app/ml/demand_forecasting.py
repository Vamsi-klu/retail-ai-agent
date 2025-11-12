"""
Demand forecasting ML module using time series analysis.
"""
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


class DemandForecaster:
    """
    Demand forecasting model for predicting product sales.
    Uses linear regression and moving averages for forecasting.
    """

    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def prepare_data(self, sales_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare sales data for training.

        Args:
            sales_data: List of sales records with date and quantity

        Returns:
            Prepared DataFrame
        """
        df = pd.DataFrame(sales_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Extract features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days

        return df

    def train(self, sales_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train the demand forecasting model.

        Args:
            sales_data: Historical sales data

        Returns:
            Training metrics
        """
        if len(sales_data) < 7:
            return {
                "status": "insufficient_data",
                "message": "Need at least 7 days of data for training"
            }

        df = self.prepare_data(sales_data)

        # Features
        X = df[['days_since_start', 'day_of_week', 'month']].values

        # Target
        y = df['quantity'].values

        # Train model
        self.model.fit(X, y)
        self.is_trained = True

        # Calculate training metrics
        predictions = self.model.predict(X)
        mse = np.mean((predictions - y) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - y))

        return {
            "status": "trained",
            "rmse": float(rmse),
            "mae": float(mae),
            "training_samples": len(df)
        }

    def predict(
        self,
        days_ahead: int = 7,
        start_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Predict future demand.

        Args:
            days_ahead: Number of days to forecast
            start_date: Starting date for prediction

        Returns:
            List of predictions with dates and quantities
        """
        if not self.is_trained:
            return []

        if start_date is None:
            start_date = datetime.utcnow()

        predictions = []
        days_since_start = 0  # Simplified for example

        for i in range(days_ahead):
            pred_date = start_date + timedelta(days=i)
            features = np.array([[
                days_since_start + i,
                pred_date.weekday(),
                pred_date.month
            ]])

            quantity = max(0, self.model.predict(features)[0])

            predictions.append({
                "date": pred_date.isoformat(),
                "predicted_quantity": round(float(quantity), 2),
                "confidence": 0.85  # Simplified confidence score
            })

        return predictions

    def calculate_reorder_point(
        self,
        average_daily_demand: float,
        lead_time_days: int,
        safety_stock_days: int = 3
    ) -> int:
        """
        Calculate optimal reorder point for a product.

        Args:
            average_daily_demand: Average daily demand
            lead_time_days: Supplier lead time in days
            safety_stock_days: Safety stock buffer in days

        Returns:
            Recommended reorder point
        """
        reorder_point = average_daily_demand * (lead_time_days + safety_stock_days)
        return int(np.ceil(reorder_point))

    def calculate_reorder_quantity(
        self,
        average_daily_demand: float,
        holding_cost_per_unit: float,
        ordering_cost: float
    ) -> int:
        """
        Calculate Economic Order Quantity (EOQ).

        Args:
            average_daily_demand: Average daily demand
            holding_cost_per_unit: Cost to hold one unit for a year
            ordering_cost: Fixed cost per order

        Returns:
            Recommended reorder quantity
        """
        annual_demand = average_daily_demand * 365

        if holding_cost_per_unit <= 0:
            return int(average_daily_demand * 30)  # Default to 30 days

        eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
        return int(np.ceil(eoq))
