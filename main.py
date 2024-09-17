import os
from pathlib import Path
from typing import Dict, List, Tuple

from models.home_buyer import HomeBuyer
from models.neighborhood import Neighborhood

BASE_DIR = Path(__file__).resolve().parent


def parse_neighborhood(line: str) -> Neighborhood:
    """
    Parses a neighborhood line from the input file and creates a Neighborhood object.
    """
    parts = line.split()
    name = parts[1]
    scores = {k: int(v) for k, v in (x.split(":") for x in parts[2:])}

    return Neighborhood(name, scores)


def parse_home_buyer(line: str) -> HomeBuyer:
    """
    Parses a home buyer line from the input file and creates a HomeBuyer object.
    """
    parts = line.split()
    name = parts[1]
    goals = {k: int(v) for k, v in (x.split(":") for x in parts[2:-1])}
    preferences = parts[-1].split(">")

    return HomeBuyer(name, goals, preferences)


def parse_input(file_path: str) -> Tuple[Dict[str, Neighborhood], List[HomeBuyer]]:
    """
    Parses the input file to extract neighborhood and home buyer data.
    """
    neighborhoods = {}
    buyers = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("N"):
                neighborhood = parse_neighborhood(line)
                neighborhoods[neighborhood.name] = neighborhood
            elif line.startswith("H"):
                home_buyer = parse_home_buyer(line)
                buyers.append(home_buyer)

    return neighborhoods, buyers


def place_home_buyers(neighborhoods: Dict[str, Neighborhood], buyers: list[HomeBuyer]):
    """
    Allocates home buyers to neighborhoods based on their preferences and fit scores.
    Each neighborhood receives an equal number of buyers, and buyers are placed
    in their most preferred neighborhood that has available space.
    """
    buyers_per_neighborhood = len(buyers) // len(neighborhoods)

    def sort_by_fit(buyer: HomeBuyer) -> int:
        return buyer.get_preferred_fit(neighborhoods)

    buyers.sort(key=sort_by_fit, reverse=True)

    for buyer in buyers:
        for preferred_neighborhood_name in buyer.preferences:
            neighborhood = neighborhoods[preferred_neighborhood_name]
            if len(neighborhood.buyers) < buyers_per_neighborhood:
                score = buyer.calc_fit(neighborhood)
                neighborhood.add_buyer(buyer, score)
                break


def write_output_file(
    neighborhoods: List[Neighborhood],
    output_file: str = "output.txt",
):
    """
    Writes the final allocation of home buyers to neighborhoods into an output file.
    """
    with open(output_file, "w") as file:
        for neighborhood in neighborhoods.values():
            file.write(f"{neighborhood}\n")  # Ensure each neighborhood is on a new line

    print("File output.txt saved.")


def load_input_file() -> str:
    """
    Prompts the user for a custom input file or defaults to './input.txt'.
    Verifies if the file exists and returns the file path.
    """
    print("Custom input file (leave blank for ./input.txt):")
    custom_input_file = input().strip()  # Avoid unnecessary whitespace
    input_file = os.path.join(BASE_DIR, custom_input_file or "input.txt")

    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found. Please check the path.")
        exit(1)

    try:
        with open(input_file, "r"):
            print(f"Successfully loaded file: {input_file}")
            return input_file
    except Exception as e:
        print(f"An error occurred while trying to read the file: {e}")
        exit(1)


if __name__ == "__main__":
    input_file = load_input_file()
    output_file = "output.txt"

    neighborhoods, buyers = parse_input(input_file)
    place_home_buyers(neighborhoods, buyers)
    write_output_file(neighborhoods, output_file)
