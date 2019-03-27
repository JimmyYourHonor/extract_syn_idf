from wikidataintegrator import wdi_core, wdi_login
from time import gmtime, strftime
import yaml

# list of items on wikidata that we are going to modify
Qid_and_gardId_pairs = {
    'Q38404': '10740',
    'Q21154076': '12388',
    'Q4552290': '5659',
    'Q21154064': '13297',
    'Q21154079': '13296'
}
prop_nr = 'P4317'
gard_ref_val = 'Q47517289'
stated_in = 'P248'

retrieved = 'P813'

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setup login for wikidata
login_instance = wdi_login.WDLogin(user=config['WIKI_DATA_USERNAME'], pwd=config['WIKI_DATA_PASSWORD'])
for QID, gard_id in Qid_and_gardId_pairs.items():
    # Create the WDString data here: data type object
    gard_ref = wdi_core.WDItemID(value=gard_ref_val, prop_nr=stated_in, is_reference=True)
    date_ref = wdi_core.WDTime(time=strftime("+%Y-%m-%dT00:00:00Z", gmtime()), prop_nr=retrieved, is_reference=True)

    references = [[gard_ref, date_ref]]
    entry_gard_id = wdi_core.WDString(value=gard_id, prop_nr=prop_nr, references=references)

    data = [entry_gard_id]
    wd_item = wdi_core.WDItemEngine(wd_item_id=QID, data=data)
    wd_item.write(login_instance)
