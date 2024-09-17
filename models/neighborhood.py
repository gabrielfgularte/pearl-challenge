from __future__ import annotations

from typing import Dict


class Neighborhood:
    def __init__(self, name: str, scores: Dict[str, int]):
        self.name = name
        self.scores = scores
        self.buyers = []

    def add_buyer(self, buyer, score: int):
        """Add a buyer to the Neighborhood."""
        self.buyers.append((buyer, score))

    def _get_score(self, buyer_info) -> int:
        """
        Helper function to extract the score of each buyer.

        Args:
            buyer_info: Tuple[HomeBuyer, int]
        """
        return buyer_info[1]

    def __repr__(self) -> str:
        sorted_buyers = sorted(self.buyers, key=self._get_score, reverse=True)
        buyers_str = " ".join(
            f"{buyer.name}({score})" for buyer, score in sorted_buyers
        )
        return f"{self.name}: {buyers_str}"
