import requests
from requests import Response
from bs4 import BeautifulSoup
from typing import *



class GridView:
  """
  A class which stores characters in a grid and allows them to be printed to 
  the console in a grid.

  Attributes:
    _empty_char (str): Character to be used as the empty cell.
    _width (int): The width of the grid in chars.
    _height (int): The height of the grid in chars.
    _grid (List[List[str]]): The underlying arrays storing each grid element.
  """
  def __init__(self):
    """
    Initialises a 1x1 GridView containing the empty character.
    """
    self._empty_char = " "
    self._width = 1
    self._height = 1
    self._grid = [[self._empty_char]]

  def __str__(self):
    string_rep = ""
    for y in range(self._height - 1, -1, -1):
      row = ""
      for x in range(self._width):
        row += f"{self.get(x, y)}"
      string_rep += f"{row}\n"
    return string_rep

  def insert(self, x: int, y: int, char: str):
    """
    Inserts a given character into the grid at the (x, y) position, expands the grid if necessary.

    Args:
      x (int): The x-position to insert to.
      y (int): The y-position to insert to.
      char (str): The character to insert.
    """
    if x >= self._width:
      # Expand grid width.
      for row_index in range(self._height):
        self._grid[row_index] += ([self._empty_char] * (x - self._width + 1))
      self._width = x + 1
    if y >= self._height:
      for _ in range(y - self._height + 1):
        self._grid.append([self._empty_char] * self._width)
      self._height = y + 1
    # Insert character
    self._grid[y][x] = char
  
  def get(self, x_pos: int, y_pos: int) -> str:
    """
    Returns the character stored at (x, y).

    Args:
      x (int): The x-position of the desired character.
      y (int): The y-position of the desired character.

    Returns:
      (str): The character stored at (x, y).
    """
    if x_pos > self._width or x_pos < 0:
      raise IndexError
    if y_pos > self._height  or y_pos < 0:
      raise IndexError
    return self._grid[y_pos][x_pos]

def get_HTTP_response(url: str) -> Response | None:
  """
  Get a response from the url.

  Args:
    url (str): The url to request a response from.

  Returns: 
    The OK response from the url.

  Raises: 
    HTTPError if the response from the url is not OK (200).
  """
  OK = 200
  
  # Check for an empty url and raise a value error if an empty one is supplied.
  if len(url) == 0: 
    raise ValueError("url cannot be empty")
  
  # Request a response from the url; if response is not OK (200) raise a HTTPError, otherwise return the response.
  response = requests.get(url)
  if (response.status_code != OK):
    print(response.raise_for_status())
    return
  else:
    return response
  
def parse_response(response: Response) -> GridView:
  """
  Parse the webpage into a GridView if the webpage has the appropriately formatted table.

  Args:
    response (Response): The OK response from a webpage.

  Returns:
    (GridView): A GridView containing the decoded message.                                                                                                           
  """
  grid_view = GridView()  # Initialise a map for the grid elements.
  
  # Parse the response to html and extract the table components to populate the grid_elems dictionary.
  soup = BeautifulSoup(response.text, 'html.parser') 
  table = soup.find ('table') 
  for row in table.find_all('tr'): 
    columns = row.find_all(['th', 'td']) 
    if (not str(columns[0].text).isdigit()): # skip the legend within the table
      continue
    grid_view.insert(int(columns[0].text), int(columns[2].text), columns[1].text) # Insert into GridView
  return grid_view

def decode_secret_message(url: str):
  """
  Decode the secret message contained within the google doc pointed to by the url.

  Args:
    url (str): The url pointing to a google doc containing input data for a secret message.
  """
  # Get a HTTP response from the webpage pointed to by the url.
  response = get_HTTP_response(url)
  # Parse the webpage to retreive the positions of each character and insert them into a GridView.
  grid_view = parse_response(response)
  # Print the GridView to console.
  print(grid_view)
  
def main():
  # Example urls
  hard_example_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
  easy_example_url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"  

  # Decode message for each url.
  decode_secret_message(easy_example_url)
  decode_secret_message(hard_example_url)  


if __name__ == "__main__":
    main()



