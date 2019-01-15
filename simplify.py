import requests

url = 'https://api.rarediseases.info.nih.gov/api/diseases'

data = requests.get(url, headers={'APIKey': '^EaR5sBRm)Qa8)6lJgT8'}).json()

# After getting data from the api
# Use a loop to iterate through the data and extract out synonyms and identifiers
list_of_diseases = []
for disease in data:
    synonyms = disease['synonyms']
    identifiers = disease['identifiers']
    item = {'synonyms': synonyms, 'identifiers': identifiers}
    item = '\n' + str(item)
    list_of_diseases.append(item)

# Now open a file and write the list that we created earlier to it.
file = open('simplified.txt', 'w')

for item in list_of_diseases:
    file.write(item)

file.close()
