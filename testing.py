from wikidataintegrator import wdi_core
QID = 'Q3899001'
query = 'select ?id where{wd:' + QID + ' wdt:P4317 ?id.}'
result = wdi_core.WDItemEngine.execute_sparql_query(query)
print(result)