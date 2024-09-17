import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import mock_open, patch

from main import (
    BASE_DIR,
    load_input_file,
    parse_home_buyer,
    parse_input,
    parse_neighborhood,
    place_home_buyers,
    write_output_file,
)
from models.home_buyer import HomeBuyer
from models.neighborhood import Neighborhood


class BaseSupressedTestCase(unittest.TestCase):
    def _suppress_err_and_outs(self):
        """
        Suppress errors (stderr) and prints (stdout) from tests.
        This helps to keep the test output cleaner by redirecting output to StringIO.
        """
        self.suppress_stdout_stderr = io.StringIO()
        self.stdout_patcher = redirect_stdout(self.suppress_stdout_stderr)
        self.stderr_patcher = redirect_stderr(self.suppress_stdout_stderr)

        self.stdout_patcher.__enter__()
        self.stderr_patcher.__enter__()

    def setUp(self):
        self._suppress_err_and_outs()

    def tearDown(self):
        self.stdout_patcher.__exit__(None, None, None)
        self.stderr_patcher.__exit__(None, None, None)
        self.suppress_stdout_stderr = None


class TestMainFunctions(BaseSupressedTestCase):

    def test_parse_neighborhood(self):
        # Test parsing of a neighborhood line
        line = "N N1 E:10 W:5 R:7"
        neighborhood = parse_neighborhood(line)
        self.assertEqual(neighborhood.name, "N1")
        self.assertEqual(neighborhood.scores["E"], 10)
        self.assertEqual(neighborhood.scores["W"], 5)
        self.assertEqual(neighborhood.scores["R"], 7)

    def test_parse_home_buyer(self):
        # Test parsing of a home buyer line
        line = "H H1 E:8 W:6 R:9 N1>N2>N3"
        home_buyer = parse_home_buyer(line)
        self.assertEqual(home_buyer.name, "H1")
        self.assertEqual(home_buyer.goals["E"], 8)
        self.assertEqual(home_buyer.goals["W"], 6)
        self.assertEqual(home_buyer.goals["R"], 9)
        self.assertEqual(home_buyer.preferences, ["N1", "N2", "N3"])

    def test_parse_input(self):
        # Test parsing an input file
        with open("test_input.txt", "w") as f:
            f.write("N N1 E:7 W:5 R:8\n")
            f.write("H H1 E:8 W:6 R:9 N1>N2\n")

        neighborhoods, buyers = parse_input("test_input.txt")
        self.assertEqual(len(neighborhoods), 1)
        self.assertEqual(len(buyers), 1)
        self.assertEqual(neighborhoods["N1"].scores["E"], 7)
        self.assertEqual(buyers[0].goals["E"], 8)

    def test_place_home_buyers(self):
        # Test placing home buyers into neighborhoods
        neighborhood1 = Neighborhood(name="N1", scores={"E": 7, "W": 5, "R": 8})
        neighborhood2 = Neighborhood(name="N2", scores={"E": 8, "W": 6, "R": 9})
        neighborhoods = {"N1": neighborhood1, "N2": neighborhood2}

        buyer1 = HomeBuyer(
            name="H1", goals={"E": 8, "W": 6, "R": 9}, preferences=["N1", "N2"]
        )
        buyer2 = HomeBuyer(
            name="H2", goals={"E": 9, "W": 5, "R": 7}, preferences=["N2", "N1"]
        )
        buyers = [buyer1, buyer2]

        place_home_buyers(neighborhoods, buyers)

        self.assertEqual(len(neighborhood1.buyers), 1)
        self.assertEqual(len(neighborhood2.buyers), 1)
        self.assertEqual(neighborhood1.buyers[0][0].name, "H1")
        self.assertEqual(neighborhood2.buyers[0][0].name, "H2")

    def test_even_distribution(self):
        # Test that buyers are evenly distributed
        neighborhood1 = Neighborhood(name="N1", scores={"E": 7, "W": 5, "R": 8})
        neighborhood2 = Neighborhood(name="N2", scores={"E": 8, "W": 6, "R": 9})
        neighborhoods = {"N1": neighborhood1, "N2": neighborhood2}

        buyers = [
            HomeBuyer(
                name=f"H{i}", goals={"E": 7, "W": 5, "R": 6}, preferences=["N1", "N2"]
            )
            for i in range(4)
        ]

        place_home_buyers(neighborhoods, buyers)

        self.assertEqual(len(neighborhood1.buyers), 2)
        self.assertEqual(len(neighborhood2.buyers), 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_output_file(self, mock_file):
        # Assert that the file was written with the correct content
        neighborhood1 = Neighborhood("N1", {"E": 7, "W": 5, "R": 8})
        neighborhood2 = Neighborhood("N2", {"E": 6, "W": 6, "R": 7})

        buyer1 = HomeBuyer("H1", {"E": 8, "W": 5, "R": 9}, ["N1", "N2"])
        buyer2 = HomeBuyer("H2", {"E": 7, "W": 6, "R": 8}, ["N2", "N1"])

        neighborhood1.add_buyer(buyer1, 150)
        neighborhood2.add_buyer(buyer2, 140)

        neighborhoods = {
            "N1": neighborhood1,
            "N2": neighborhood2,
        }

        write_output_file(neighborhoods, output_file="output.txt")

        handle = mock_file()
        handle.write.assert_any_call("N1: H1(150)\n")
        handle.write.assert_any_call("N2: H2(140)\n")

    @patch("builtins.input", return_value="input.txt")
    def test_sample_input_output(self, mock_input):
        input_file = load_input_file()
        output_file = "test_output.txt"
        neighborhoods, buyers = parse_input(input_file)
        place_home_buyers(neighborhoods, buyers)
        write_output_file(neighborhoods, output_file)

        expected_output = """N0: H5(161) H11(154) H2(128) H4(122)
N1: H9(23) H8(21) H7(20) H1(18)
N2: H6(128) H3(120) H10(86) H0(83)
        """

        with open(os.path.join(BASE_DIR, output_file)) as f:
            s = f.read()

        assert s == expected_output


class TestMainErrorHandling(BaseSupressedTestCase):

    # Test invalid lines on parse_neighborhood
    def test_parse_neighborhood_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_neighborhood("N N1 E:invalid W:5 R:8")

    # Test invalid lines on parse_home_buyer
    def test_parse_home_buyer_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_home_buyer("H H1 E:8 W:invalid R:9 N1>N2")

    # Test invalid or not found files on load_input_file
    @patch("builtins.input", return_value="non_existent_file.txt")
    def test_load_input_file_not_found(self, mock_input):
        with self.assertRaises(
            SystemExit
        ):  # load_input_file should exit if file doesn't exist
            with redirect_stderr(
                io.StringIO()
            ):  # redirect stderr to supress output while testing
                load_input_file()

    # Test if load_input_file successfull returns a file
    @patch("builtins.input", return_value="")
    @patch("os.path.exists", return_value=True)
    def test_load_input_file_exists(self, mock_exists, mock_input):
        file_path = load_input_file()
        self.assertEqual(file_path, os.path.join(BASE_DIR, "input.txt"))

    # Test empty files on parse_input
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_parse_input_empty_file(self, mock_file):
        neighborhoods, buyers = parse_input("input.txt")
        self.assertEqual(len(neighborhoods), 0)
        self.assertEqual(len(buyers), 0)

    # Test invalid neighborhood
    def test_place_home_buyers_invalid_preference(self):
        neighborhood1 = Neighborhood(name="N1", scores={"E": 7, "W": 5, "R": 8})
        neighborhoods = {"N1": neighborhood1}

        buyer = HomeBuyer(name="H1", goals={"E": 8, "W": 6, "R": 9}, preferences=["N2"])
        buyers = [buyer]

        with self.assertRaises(KeyError):
            place_home_buyers(neighborhoods, buyers)


if __name__ == "__main__":
    unittest.main()
