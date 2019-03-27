from wikidataintegrator import wdi_core
import requests
import csv
url = 'https://api.rarediseases.info.nih.gov/api/diseases'

data = requests.get(url, headers={'APIKey': '^EaR5sBRm)Qa8)6lJgT8'}).json()
# First get data about rare diseases from the API.

with open('diseaseOrganize.csv', 'w') as csv_file:
    # Open up a csv file and a writer for the csv file
    fieldnames = ['Gard ID', 'identifiers', 'Number of Matches', 'QID', 'Match Gard ID']
    writer = csv.DictWriter(csv_file, fieldnames, delimiter=',', lineterminator='\n')
    writer.writeheader()
    # looping through every item returned from gard rare diseases
    for item in data:
        # gard id for this disease
        gardId = str(item['diseaseId'])
        synonyms = item['synonyms']
        # list of synonyms that this item has
        identifiers = item['identifiers']
        identifiers_str = ''
        # list of identifiers that this item has (including 3 types: OMIM, UMLS, and ORPANET)

        set_of_results = set()

        # for each identifier send a query to wikidata
        # And add the resulting items list to set of results
        for idf in identifiers:
            identifiers_str = identifiers_str + idf['identifierType'] + ':' + idf['identifierId'] + ' | '
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
            query = 'SELECT ?item WHERE{ ?item wdt:' + predicate + ' \"' + idf['identifierId'] + '\";'+'p:'+predicate+' ?a. optional{?a pq:P4390 ?q}. filter(!bound(?q) || ?q = wd:Q39893449)}'
            result = wdi_core.WDItemEngine.execute_sparql_query(query)
            for uri in result['results']['bindings']:
                set_of_results.add(uri['item']['value'])

        match = ''
        if len(set_of_results) == 1:
            QID = set_of_results.pop()
            set_of_results.add(QID)
            QID = QID[31:]
            query = 'select ?id where{wd:' + QID + ' wdt:P4317 ?id.}'
            result = wdi_core.WDItemEngine.execute_sparql_query(query)
            if len(result['results']['bindings']) > 1:
                match = ' has more than one gard id'
            elif len(result['results']['bindings']) == 1 and result['results']['bindings'][0]['id']['value'] == gardId:
                match = 'True'
            else:
                match = 'False'
                # Here is where we add the gard entry to wikidata

        num_of_matches = str(len(set_of_results))
        QIDs = ''
        while len(set_of_results) != 0:
            q_number = set_of_results.pop()[31:]
            QIDs = QIDs + str(q_number) + ' | '
        identifiers_str = identifiers_str[:len(identifiers_str)-1]
        writer.writerow({'Gard ID': gardId, 'identifiers': identifiers_str, 'Number of Matches': num_of_matches,
                         'QID': QIDs, 'Match Gard ID': match})
