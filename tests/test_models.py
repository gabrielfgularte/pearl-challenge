import unittest

from models.home_buyer import HomeBuyer
from models.neighborhood import Neighborhood


class TestModels(unittest.TestCase):

    def test_home_buyer_creation(self):
        # Test the creation of a HomeBuyer object
        buyer = HomeBuyer(name="H1", goals={"E": 8, "W": 5, "R": 7}, preferences=["N1", "N2"])
        self.assertEqual(buyer.name, "H1")
        self.assertEqual(buyer.goals["E"], 8)
        self.assertEqual(buyer.preferences, ["N1", "N2"])

    def test_neighborhood_creation(self):
        # Test the creation of a Neighborhood object
        neighborhood = Neighborhood(name="N1", scores={"E": 10, "W": 4, "R": 6})
        self.assertEqual(neighborhood.name, "N1")
        self.assertEqual(neighborhood.scores["E"], 10)

    def test_calc_fit(self):
        # Test the calc_fit method of HomeBuyer
        buyer = HomeBuyer(name="H1", goals={"E": 8, "W": 5, "R": 7}, preferences=["N1", "N2"])
        neighborhood = Neighborhood(name="N1", scores={"E": 7, "W": 3, "R": 10})
        fit_score = buyer.calc_fit(neighborhood)

        # Dot product calculation between HomeBuyer.goals and Neighborhood.scores vectors.
        expected_score = (8 * 7) + (5 * 3) + (7 * 10)

        self.assertEqual(fit_score, expected_score)

    def test_add_buyer_to_neighborhood(self):
        # Test adding a buyer to a neighborhood and check if the buyer is stored correctly
        neighborhood = Neighborhood(name="N1", scores={"E": 7, "W": 3, "R": 10})
        buyer = HomeBuyer(name="H1", goals={"E": 8, "W": 5, "R": 7}, preferences=["N1", "N2"])
        neighborhood.add_buyer(buyer, 200)
        self.assertEqual(len(neighborhood.buyers), 1)
        self.assertEqual(neighborhood.buyers[0][0], buyer)
        self.assertEqual(neighborhood.buyers[0][1], 200)


if __name__ == "__main__":
    unittest.main()
