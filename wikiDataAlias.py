from wikidataintegrator import wdi_core
import requests
import csv
url = 'https://api.rarediseases.info.nih.gov/api/diseases'

data = requests.get(url, headers={'APIKey': '^EaR5sBRm)Qa8)6lJgT8'}).json()
# First get data about rare diseases from the API.

with open('diseaseOrganize.csv', 'w') as csv_file:
    # Open up a csv file and a writer for the csv file
    fieldnames = ['Gard ID', 'identifiers', 'Number of Matches', 'QID']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()
    # looping through every item returned from gard rare diseases
    for item in data:
        # gard id for this disease
        gardId = item['diseaseId']
        synonyms = item['synonyms']
        # list of synonyms that this item has
        identifiers = item['identifiers']
        # list of identifiers that this item has (including 3 types: OMIM, UMLS, and ORPANET)
        set_of_results = set()

        # for each identifier send a query to wikidata
        # And add the resulting items list to set of results
        for idf in identifiers:
            predicate = ''
            if idf['identifierType'] == 'OMIM':
                predicate = 'P492'
            elif idf['identifierType'] == 'ORPHANET':
                predicate = 'P1550'
            elif idf['identifierType'] == 'UMLS':
                predicate = 'P2892'
            elif idf['identifierType'] == 'SNOMED CT':
                predicate = 'P5806'
            elif idf['identifierType'] == 'ICD 10':
                predicate = 'P494'
            elif idf['identifierType'] == 'NCI Thesaurus':
                predicate = 'P1748'
            elif idf['identifierType'] == 'ICD 10-CM':
                predicate = 'P4229'
            elif idf['identifierType'] == 'MeSH':
                predicate = 'P486'
            elif idf['identifierType'] == 'ICD 9':
                predicate = 'P493'
            else:
                print('New identifierType ' + idf['identifierType'])
                exit(1)
            query = 'SELECT ?item WHERE{ ?item wdt:' + predicate + '\"' + idf['identifierId'] + '\"}'
            result = wdi_core.WDItemEngine.execute_sparql_query(query)
            for uri in result['results']['bindings']:
                set_of_results.add(uri['item']['value'])

        #if len(set_of_results) == 0:
            # This rare disease didn't find any match for any identifier
            # or it doesn't have any identifier
        #   file.write('Item with identifiers ' + str(identifiers) + ' didn\'t find any match\n')
        #elif len(set_of_results) == 1:
            # These are the items that we are suppose to modify.
            # First get their Q numbers
        #    q_number = set_of_results.pop()[31:]
        #    file.write('Item to be modified ' + q_number + '\n')
        #else:
        #    file.write('Item with identifiers ' + str(identifiers) + ' found too much matches\n')


#file.close()
