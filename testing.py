import requests
url = 'https://api.rarediseases.info.nih.gov/api/diseases'

data = requests.get(url, headers={'APIKey': '^EaR5sBRm)Qa8)6lJgT8'}).json()

print(str(data))
