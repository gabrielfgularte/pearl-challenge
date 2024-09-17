from typing import Dict, List

from .neighborhood import Neighborhood


class HomeBuyer:
    def __init__(self, name: str, goals: Dict[str, int], preferences: List[str]):
        self.name = name
        self.goals = goals
        self.preferences = preferences

    def calc_fit(self, neighborhood: Neighborhood) -> int:
        """Calc 'fit' based on buyer goals and Neighborhood."""
        return sum(self.goals.get(key, 0) * neighborhood.scores.get(key, 0) for key in self.goals)

    def get_preferred_fit(self, neighborhoods: dict[str, Neighborhood]) -> int:
        """Calculates the fit score for the buyer's most preferred neighborhood."""
        preferred_neighborhood = neighborhoods[self.preferences[0]]
        return self.calc_fit(preferred_neighborhood)

    def __repr__(self):
        return self.name
