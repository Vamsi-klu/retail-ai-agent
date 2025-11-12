"""
Unit tests for ML modules.
"""
import pytest
from app.ml.demand_forecasting import DemandForecaster
from app.ml.customer_segmentation import CustomerSegmenter
from app.ml.churn_prediction import ChurnPredictor
from app.ml.pricing_optimizer import PricingOptimizer


@pytest.mark.unit
def test_demand_forecaster_prediction():
    """Test demand forecasting."""
    forecaster = DemandForecaster()

    # Create sample sales data
    sales_data = [
        {"date": "2024-01-01", "quantity": 10},
        {"date": "2024-01-02", "quantity": 15},
        {"date": "2024-01-03", "quantity": 12},
        {"date": "2024-01-04", "quantity": 18},
        {"date": "2024-01-05", "quantity": 20},
        {"date": "2024-01-06", "quantity": 14},
        {"date": "2024-01-07", "quantity": 16},
    ]

    # Train model
    result = forecaster.train(sales_data)
    assert result["status"] == "trained"

    # Make predictions
    predictions = forecaster.predict(days_ahead=3)
    assert len(predictions) == 3
    assert all("predicted_quantity" in p for p in predictions)


@pytest.mark.unit
def test_demand_forecaster_reorder_point():
    """Test reorder point calculation."""
    forecaster = DemandForecaster()

    reorder_point = forecaster.calculate_reorder_point(
        average_daily_demand=10.0,
        lead_time_days=5,
        safety_stock_days=3
    )

    assert reorder_point == 80  # 10 * (5 + 3)


@pytest.mark.unit
def test_customer_segmenter():
    """Test customer segmentation."""
    segmenter = CustomerSegmenter(n_segments=4)

    # Create sample customer data
    customer_data = [
        {"id": 1, "recency_score": 8, "frequency_score": 7, "monetary_score": 9},
        {"id": 2, "recency_score": 3, "frequency_score": 2, "monetary_score": 3},
        {"id": 3, "recency_score": 6, "frequency_score": 6, "monetary_score": 5},
        {"id": 4, "recency_score": 2, "frequency_score": 1, "monetary_score": 2},
    ]

    # Train model
    result = segmenter.train(customer_data)
    assert result["status"] == "trained"

    # Predict segment
    prediction = segmenter.predict(customer_data[0])
    assert "segment" in prediction
    assert "segment_label" in prediction
    assert "confidence" in prediction


@pytest.mark.unit
def test_churn_predictor_rule_based():
    """Test churn prediction with rule-based fallback."""
    predictor = ChurnPredictor()

    # Test with recent purchase (low churn risk)
    customer_data = {
        "id": 1,
        "last_purchase_date": "2024-01-15",
        "recency_score": 8,
        "frequency_score": 7,
        "total_purchases": 1000,
        "total_orders": 10
    }

    prediction = predictor.predict(customer_data)
    assert "churn_probability" in prediction
    assert "risk_level" in prediction
    assert prediction["churn_probability"] >= 0
    assert prediction["churn_probability"] <= 1


@pytest.mark.unit
def test_pricing_optimizer():
    """Test pricing optimization."""
    optimizer = PricingOptimizer()

    result = optimizer.calculate_optimal_price(
        cost_price=50.0,
        current_demand=70.0,
        competitor_price=80.0,
        stock_level=100,
        reorder_point=20,
        is_seasonal=True,
        season_factor=1.2
    )

    assert "optimal_price" in result
    assert "profit_margin" in result
    assert "recommendation" in result
    assert result["optimal_price"] > 50.0  # Above cost


@pytest.mark.unit
def test_pricing_optimizer_discount():
    """Test discount calculation."""
    optimizer = PricingOptimizer()

    result = optimizer.calculate_discount(
        base_price=100.0,
        quantity=50,
        customer_tier="gold"
    )

    assert "final_price" in result
    assert "total_discount_pct" in result
    assert result["final_price"] < 100.0  # Discounted
