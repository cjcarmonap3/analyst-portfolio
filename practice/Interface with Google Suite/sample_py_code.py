import requests
from bs4 import BeautifulSoup

def print_unicode_message(url):
    # get information from the URL
    response = requests.get(url)

    # parse out table in the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    data = []

    # configure the table as shown in the Google Doc
    for row in rows[1:]: ## skips the header row
        cells = row.find_all(["td"])
        if len(cells) < 3:
            print("Skipping row due to insufficient cells:", row)
            continue

        # extract the x_coordinate, character, and y_coordinate from the cells in proper data types
        x_coordinate = int(cells[0].get_text(strip=True))
        character = cells[1].get_text(strip=True)
        y_coordinate = int(cells[2].get_text(strip=True))

        data.append([x_coordinate, character, y_coordinate])

    # find the maximum x and y coordinates to determine the size of the grid
    max_x = max(x_coordinate for x_coordinate, _, _ in data)
    max_y = max(y_coordinate for _, _, y_coordinate in data)

    # create a grid of spaces with the appropriate dimensions
    grid = [
        [" "] * (max_x + 1) for _ in range(max_y + 1)
    ]

    # plot the grid with unicode characters
    for x_coordinate, character, y_coordinate in data:
        grid[y_coordinate][x_coordinate] = character

    # print the grid in reverse order to match the expected output
    print("\n".join(
        "".join(row)
        for row in reversed(grid)
    ))

''' USE THIS URL TO TEST EXAMPLE
url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
'''

url = "https://docs.google.com/document/d/e/2PACX-1vQiVT_Jj04V35C-YRzvoqyEYYzdXHcRyMUZCVQRYCu6gQJX7hbNhJ5eFCMuoX47cAsDW2ZBYppUQITr/pub"
print_unicode_message(url)
