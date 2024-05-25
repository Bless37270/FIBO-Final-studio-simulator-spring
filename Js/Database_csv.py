from bs4 import BeautifulSoup
import pandas as pd

with open('Inputpage.html', 'r') as file:
    Inputpage = file.read()

soup = BeautifulSoup(Inputpage, 'html.parser')

targetz = soup.find("span", class_="coordinate-of-target2").text.strip()
targety = soup.find("span", class_="coordinate-of-target3").text.strip()
posx = soup.find("span", class_="coordinate-of-targetx").text.strip()
posy = soup.find("span", class_="coordinate-of-targety").text.strip()
posz = soup.find("span", class_="coordinate-of-targetz").text.strip()

output_angle = 0
output_posy = 0
output_velocity = 0

# Create DataFrame
data = {
    'targetz': [targetz],
    'targety': [targety],
    'posx': [posx],
    'posy': [posy],
    'posz': [posz],
    'output_angle': [output_angle],
    'output_posy': [output_posy],
    'output_velocity': [output_velocity]
}

df = pd.DataFrame(data)

df.to_csv('output.csv', index=False)
