import requests
from bs4 import BeautifulSoup


# Iterate over the years
#for i in range(1, 25):
for i in range(24, 25):
  URL = "https://sites.google.com/site/wheeloffortunepuzzlecompendium/home/compendium/season-" + str(i) + "-compendium"
  page = requests.get(URL)

  #print(page.text)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="sites-canvas-main-content")
  print(results.prettify())
