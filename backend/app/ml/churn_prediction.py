"""
Customer churn prediction ML module.
"""
from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta


class ChurnPredictor:
    """
    Churn prediction model using Random Forest classifier.
    Predicts probability of customer churn based on behavioral features.
    """

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, customer_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare customer features for churn prediction.

        Args:
            customer_data: List of customer records

        Returns:
            DataFrame with features
        """
        df = pd.DataFrame(customer_data)

        # Calculate derived features
        if 'last_purchase_date' in df.columns:
            df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
            df['days_since_purchase'] = (
                datetime.utcnow() - df['last_purchase_date']
            ).dt.days
        else:
            df['days_since_purchase'] = 0

        # Fill missing values
        df['total_purchases'] = df.get('total_purchases', 0).fillna(0)
        df['total_orders'] = df.get('total_orders', 0).fillna(0)
        df['recency_score'] = df.get('recency_score', 0).fillna(0)
        df['frequency_score'] = df.get('frequency_score', 0).fillna(0)
        df['monetary_score'] = df.get('monetary_score', 0).fillna(0)

        return df

    def train(
        self,
        customer_data: List[Dict[str, Any]],
        labels: List[int]
    ) -> Dict[str, Any]:
        """
        Train the churn prediction model.

        Args:
            customer_data: Customer features
            labels: Churn labels (1 = churned, 0 = active)

        Returns:
            Training metrics
        """
        if len(customer_data) < 10:
            return {
                "status": "insufficient_data",
                "message": "Need at least 10 customers with labels for training"
            }

        df = self.prepare_features(customer_data)

        # Select features
        feature_columns = [
            'days_since_purchase',
            'total_purchases',
            'total_orders',
            'recency_score',
            'frequency_score',
            'monetary_score'
        ]

        X = df[feature_columns].values
        y = np.array(labels)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True

        # Calculate training metrics
        train_accuracy = self.model.score(X_scaled, y)

        # Feature importance
        feature_importance = dict(zip(
            feature_columns,
            self.model.feature_importances_.tolist()
        ))

        return {
            "status": "trained",
            "accuracy": float(train_accuracy),
            "feature_importance": feature_importance,
            "training_samples": len(df)
        }

    def predict(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict churn probability for a customer.

        Args:
            customer_data: Customer features

        Returns:
            Churn prediction with probability
        """
        if not self.is_trained:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(customer_data)

        # Prepare features
        df = self.prepare_features([customer_data])

        feature_columns = [
            'days_since_purchase',
            'total_purchases',
            'total_orders',
            'recency_score',
            'frequency_score',
            'monetary_score'
        ]

        X = df[feature_columns].values

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict
        churn_prob = self.model.predict_proba(X_scaled)[0][1]

        # Risk level
        if churn_prob >= 0.7:
            risk_level = "high"
        elif churn_prob >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "churn_probability": float(churn_prob),
            "risk_level": risk_level,
            "model_type": "random_forest"
        }

    def _rule_based_prediction(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback rule-based churn prediction when model is not trained.

        Args:
            customer_data: Customer features

        Returns:
            Churn prediction
        """
        # Calculate days since last purchase
        last_purchase = customer_data.get('last_purchase_date')
        if last_purchase:
            if isinstance(last_purchase, str):
                last_purchase = datetime.fromisoformat(last_purchase.replace('Z', '+00:00'))
            days_since = (datetime.utcnow() - last_purchase).days
        else:
            days_since = 365

        # Simple rules
        recency_score = customer_data.get('recency_score', 0)
        frequency_score = customer_data.get('frequency_score', 0)

        # Calculate churn probability
        if days_since > 180:
            churn_prob = 0.9
        elif days_since > 90:
            churn_prob = 0.7
        elif days_since > 60:
            churn_prob = 0.5
        elif recency_score < 3:
            churn_prob = 0.6
        elif frequency_score < 2:
            churn_prob = 0.4
        else:
            churn_prob = 0.2

        # Risk level
        if churn_prob >= 0.7:
            risk_level = "high"
        elif churn_prob >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "churn_probability": churn_prob,
            "risk_level": risk_level,
            "model_type": "rule_based"
        }

    def batch_predict(
        self,
        customers_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Predict churn for multiple customers.

        Args:
            customers_data: List of customer records

        Returns:
            List of predictions
        """
        predictions = []
        for customer in customers_data:
            pred = self.predict(customer)
            pred['customer_id'] = customer.get('id')
            predictions.append(pred)

        return predictions
