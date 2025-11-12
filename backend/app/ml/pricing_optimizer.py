"""
Dynamic pricing optimization ML module.
"""
from typing import Dict, Any, Optional
import numpy as np


class PricingOptimizer:
    """
    Dynamic pricing optimizer using demand elasticity and market conditions.
    """

    def __init__(self):
        self.base_markup = 0.3  # 30% markup
        self.price_elasticity = -1.5  # Price elasticity of demand

    def calculate_optimal_price(
        self,
        cost_price: float,
        current_demand: float,
        competitor_price: Optional[float] = None,
        stock_level: int = 100,
        reorder_point: int = 20,
        is_seasonal: bool = False,
        season_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate optimal selling price based on multiple factors.

        Args:
            cost_price: Product cost price
            current_demand: Current demand level
            competitor_price: Competitor's price (if available)
            stock_level: Current stock level
            reorder_point: Reorder point threshold
            is_seasonal: Whether product is seasonal
            season_factor: Seasonal adjustment factor (> 1 for high season)

        Returns:
            Pricing recommendation
        """
        # Base price with markup
        base_price = cost_price * (1 + self.base_markup)

        # Demand-based adjustment
        demand_factor = self._calculate_demand_factor(current_demand)

        # Stock-based adjustment
        stock_factor = self._calculate_stock_factor(stock_level, reorder_point)

        # Competitive adjustment
        competitive_factor = self._calculate_competitive_factor(
            base_price, competitor_price
        )

        # Seasonal adjustment
        seasonal_factor = season_factor if is_seasonal else 1.0

        # Calculate optimal price
        optimal_price = (
            base_price
            * demand_factor
            * stock_factor
            * competitive_factor
            * seasonal_factor
        )

        # Ensure price is above cost
        optimal_price = max(optimal_price, cost_price * 1.05)  # Minimum 5% markup

        # Calculate potential profit
        profit_margin = ((optimal_price - cost_price) / optimal_price) * 100

        # Price change recommendation
        price_change_pct = ((optimal_price - base_price) / base_price) * 100

        return {
            "optimal_price": round(optimal_price, 2),
            "base_price": round(base_price, 2),
            "price_change_percentage": round(price_change_pct, 2),
            "profit_margin": round(profit_margin, 2),
            "factors": {
                "demand_factor": round(demand_factor, 3),
                "stock_factor": round(stock_factor, 3),
                "competitive_factor": round(competitive_factor, 3),
                "seasonal_factor": round(seasonal_factor, 3)
            },
            "recommendation": self._get_recommendation(price_change_pct)
        }

    def _calculate_demand_factor(self, demand: float) -> float:
        """
        Calculate demand-based price adjustment factor.

        Args:
            demand: Current demand level (0-100 scale)

        Returns:
            Adjustment factor
        """
        # High demand -> increase price
        # Low demand -> decrease price
        if demand > 80:
            return 1.15  # 15% increase
        elif demand > 60:
            return 1.08  # 8% increase
        elif demand < 20:
            return 0.85  # 15% decrease
        elif demand < 40:
            return 0.92  # 8% decrease
        else:
            return 1.0

    def _calculate_stock_factor(
        self,
        stock_level: int,
        reorder_point: int
    ) -> float:
        """
        Calculate stock-based price adjustment factor.

        Args:
            stock_level: Current stock
            reorder_point: Reorder threshold

        Returns:
            Adjustment factor
        """
        if stock_level <= reorder_point:
            # Low stock -> increase price to slow demand
            return 1.10
        elif stock_level > reorder_point * 5:
            # Overstock -> decrease price to move inventory
            return 0.90
        else:
            return 1.0

    def _calculate_competitive_factor(
        self,
        our_price: float,
        competitor_price: Optional[float]
    ) -> float:
        """
        Calculate competitive price adjustment factor.

        Args:
            our_price: Our current price
            competitor_price: Competitor's price

        Returns:
            Adjustment factor
        """
        if competitor_price is None or competitor_price <= 0:
            return 1.0

        price_diff_pct = ((our_price - competitor_price) / competitor_price) * 100

        # If we're significantly more expensive, consider lowering price
        if price_diff_pct > 15:
            return 0.95
        # If we're cheaper, we can increase price slightly
        elif price_diff_pct < -10:
            return 1.05
        else:
            return 1.0

    def _get_recommendation(self, price_change_pct: float) -> str:
        """
        Get pricing recommendation text.

        Args:
            price_change_pct: Percentage price change

        Returns:
            Recommendation string
        """
        if price_change_pct > 10:
            return "Significant price increase recommended due to high demand"
        elif price_change_pct > 3:
            return "Moderate price increase recommended"
        elif price_change_pct < -10:
            return "Significant price decrease recommended to move inventory"
        elif price_change_pct < -3:
            return "Moderate price decrease recommended"
        else:
            return "Current pricing is optimal"

    def calculate_discount(
        self,
        base_price: float,
        quantity: int,
        customer_tier: str = "bronze"
    ) -> Dict[str, Any]:
        """
        Calculate volume or loyalty discount.

        Args:
            base_price: Base selling price
            quantity: Purchase quantity
            customer_tier: Customer loyalty tier

        Returns:
            Discount information
        """
        # Volume discount
        if quantity >= 100:
            volume_discount = 0.15
        elif quantity >= 50:
            volume_discount = 0.10
        elif quantity >= 20:
            volume_discount = 0.05
        else:
            volume_discount = 0.0

        # Loyalty discount
        loyalty_discounts = {
            "platinum": 0.15,
            "gold": 0.10,
            "silver": 0.05,
            "bronze": 0.0
        }
        loyalty_discount = loyalty_discounts.get(customer_tier.lower(), 0.0)

        # Total discount (don't stack more than 25%)
        total_discount = min(volume_discount + loyalty_discount, 0.25)

        discount_amount = base_price * total_discount
        final_price = base_price - discount_amount

        return {
            "base_price": round(base_price, 2),
            "volume_discount_pct": round(volume_discount * 100, 2),
            "loyalty_discount_pct": round(loyalty_discount * 100, 2),
            "total_discount_pct": round(total_discount * 100, 2),
            "discount_amount": round(discount_amount, 2),
            "final_price": round(final_price, 2)
        }
