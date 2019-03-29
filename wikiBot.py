from wikidataintegrator import wdi_core, wdi_login
from time import gmtime, strftime
import time
import csv
import yaml

# Setting up
# gard property number
prop_nr = 'P4317'
# gard wiki item id
gard_ref_val = 'Q47517289'
stated_in = 'P248'
retrieved = 'P813'
# read the configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
# log in to wiki data
login_instance = wdi_login.WDLogin(user=config['BOT_USERNAME'], pwd=config['BOT_PASSWORD'])

# read the disease organize file and modify items on wikidata
with open('diseaseOrganize.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    count = 0
    for row in csv_reader:
        if line_count > 0:
            if row['Match Gard ID'] == 'False' and count < 50:
                gard_id = row['Gard ID']
                QID = row['QID']
                QID = QID[:len(QID) - 3]
                # Create the reference objects
                gard_ref = wdi_core.WDItemID(value=gard_ref_val, prop_nr=stated_in, is_reference=True)
                date_ref = wdi_core.WDTime(time=strftime("+%Y-%m-%dT00:00:00Z", gmtime()), prop_nr=retrieved,
                                           is_reference=True)
                # add reference to list of references
                references = [[gard_ref, date_ref]]
                # Create the gard id entry
                entry_gard_id = wdi_core.WDString(value=gard_id, prop_nr=prop_nr, references=references)

                data = [entry_gard_id]
                # Create the item and write to wikidata
                wd_item = wdi_core.WDItemEngine(wd_item_id=QID, data=data)
                print(f'{count}, {QID}')
                wd_item.write(login_instance)
                # wait 3 sec after writing
                time.sleep(3)
                count += 1

        line_count += 1
