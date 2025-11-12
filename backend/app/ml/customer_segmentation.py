"""
Customer segmentation ML module using clustering algorithms.
"""
from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerSegmenter:
    """
    Customer segmentation model using K-means clustering.
    Segments customers based on RFM (Recency, Frequency, Monetary) analysis.
    """

    def __init__(self, n_segments: int = 4):
        self.n_segments = n_segments
        self.model = KMeans(n_clusters=n_segments, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, customer_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare customer features for segmentation.

        Args:
            customer_data: List of customer records

        Returns:
            DataFrame with features
        """
        df = pd.DataFrame(customer_data)

        # Ensure required columns
        required_cols = ['recency_score', 'frequency_score', 'monetary_score']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0.0

        return df

    def train(self, customer_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train the customer segmentation model.

        Args:
            customer_data: Customer data with RFM scores

        Returns:
            Training metrics
        """
        if len(customer_data) < self.n_segments:
            return {
                "status": "insufficient_data",
                "message": f"Need at least {self.n_segments} customers for {self.n_segments} segments"
            }

        df = self.prepare_features(customer_data)

        # Features for clustering
        X = df[['recency_score', 'frequency_score', 'monetary_score']].values

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled)
        self.is_trained = True

        # Calculate metrics
        inertia = self.model.inertia_
        labels = self.model.labels_

        # Segment distribution
        unique, counts = np.unique(labels, return_counts=True)
        segment_distribution = dict(zip(unique.tolist(), counts.tolist()))

        return {
            "status": "trained",
            "inertia": float(inertia),
            "n_segments": self.n_segments,
            "segment_distribution": segment_distribution,
            "training_samples": len(df)
        }

    def predict(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict customer segment.

        Args:
            customer_data: Customer RFM scores

        Returns:
            Segment prediction with metadata
        """
        if not self.is_trained:
            return {"segment": 0, "confidence": 0.0}

        # Prepare features
        features = np.array([[
            customer_data.get('recency_score', 0),
            customer_data.get('frequency_score', 0),
            customer_data.get('monetary_score', 0)
        ]])

        # Scale features
        features_scaled = self.scaler.transform(features)

        # Predict segment
        segment = self.model.predict(features_scaled)[0]

        # Calculate distance to centroid as confidence proxy
        distances = self.model.transform(features_scaled)[0]
        min_distance = distances[segment]
        max_distance = np.max(distances)

        confidence = 1.0 - (min_distance / max_distance) if max_distance > 0 else 1.0

        # Assign segment label
        segment_labels = ["High Value", "Promising", "At Risk", "Lost"]
        segment_label = segment_labels[min(int(segment), len(segment_labels) - 1)]

        return {
            "segment": int(segment),
            "segment_label": segment_label,
            "confidence": float(confidence),
            "characteristics": self._get_segment_characteristics(segment)
        }

    def _get_segment_characteristics(self, segment: int) -> Dict[str, str]:
        """Get characteristics of a segment."""
        characteristics_map = {
            0: {
                "description": "High-value customers with frequent purchases",
                "action": "Maintain relationship with exclusive offers"
            },
            1: {
                "description": "Promising customers with growth potential",
                "action": "Nurture with targeted campaigns"
            },
            2: {
                "description": "Customers at risk of churning",
                "action": "Re-engage with win-back campaigns"
            },
            3: {
                "description": "Inactive or lost customers",
                "action": "Consider reactivation strategies"
            }
        }
        return characteristics_map.get(segment, {"description": "Unknown", "action": "Analyze further"})

    def batch_predict(
        self,
        customers_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Predict segments for multiple customers.

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
