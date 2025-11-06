import requests

from tqdm import tqdm
import jsonlines, json
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.parse import unquote


### Functions to retrieve wiki ids and related information

def get_wikidata_ids_from_entity_names(entity_list, output_path):
    #wiki_ids = []
    unresolved_enities = 0

    with open(output_path, 'a') as wiki_f:
        print("Writing Wikidata ids to", output_path)
        # For each entity name, get the Wikidata ID from the Wikipedia API
        for i, subject in enumerate(tqdm(entity_list, miniters=int(len(entity_list)/200))):
            if "&amp" in subject:
                subject = unquote(subject.split("title=")[-1].split("&amp")[0])
            url = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'titles': subject.strip(),
                'prop': 'pageprops',
                'ppprop': 'wikibase_item'
            }
            response = requests.get(url, params=params).json()
            try:
                wiki_id = \
                    response["query"]["pages"][next(iter(response["query"]["pages"].keys()))]["pageprops"][
                        "wikibase_item"]
            except:
                try:
                    tmp_response = response["query"]["pages"]
                    pageid = next(iter(tmp_response.keys()))
                    new_params = {
                        'action': 'query',
                        'format': 'json',
                        'pageids': pageid,
                        'prop': 'pageprops',
                        'ppprop': 'wikibase_item',
                        'redirects': ''
                    }
                    new_response = requests.get(url, params=new_params).json()
                    wiki_id = \
                        new_response["query"]["pages"][next(iter(new_response["query"]["pages"].keys()))]["pageprops"][
                            "wikibase_item"]
                    #wiki_ids += [wiki_id]
                    wiki_f.write(wiki_id + "\n")
                except:
                    unresolved_enities += 1
                    print("Failed to resolve", subject)
    return unresolved_enities


def get_wikidata_properties_from_id(wikidata_ids, output_path):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="bench-gap")
    #wikidata_metadata_list = []
    with jsonlines.open(output_path, 'w') as jsonl_file:
        print("Writing Wikidata properties to", output_path)
        for wikidata_id in tqdm(wikidata_ids, miniters=int(len(wikidata_ids)/200)):
            service = """{ bd:serviceParam wikibase:language "en". }"""
            sparql.setQuery(f""" 
                                  SELECT DISTINCT  ?item ?itemLabel ?itemDescription ?instanceOf ?countryOfOrigin ?country ?locatedIn ?location ?countryOfCitizenship ?placeOfBirth ?coordinates ?inception ?startTime ?pointInTime ?dateOfDeath ?gender ?occupation ?ethnicity ?religion (SAMPLE(?dateOfBirth) AS ?DRSample) (SAMPLE(?article) AS ?articleSample) 
                                  WHERE
                                  {{
                                  ?article  schema:about       ?item ;
                                  schema:inLanguage  "en" ;
                                  schema:isPartOf    <https://en.wikipedia.org/>
                  FILTER ( ?item = <http://www.wikidata.org/entity/{wikidata_id}> )
                  OPTIONAL
                    {{ ?item  wdt:P31 ?instanceOf}}
                  OPTIONAL
                    {{ ?item  wdt:P495 ?countryOfOrigin }}
                  OPTIONAL
                    {{ ?item  wdt:P17 ?country }}
                  OPTIONAL
                  {{ ?item  wdt:P706 ?locatedIn }}
                  OPTIONAL
                  {{ ?item  wdt:P276 ?location }}
                  OPTIONAL
                    {{ ?item  wdt:P27 ?countryOfCitizenship }}
                  OPTIONAL
                    {{ ?item  wdt:P19 ?placeOfBirth }}
                  OPTIONAL
                    {{ ?item  wdt:P625 ?coordinates }}
                  OPTIONAL
                    {{ ?item  wdt:P571 ?inception }}
                  OPTIONAL
                    {{ ?item  wdt:P580 ?startTime }}
                  OPTIONAL
                    {{ ?item  wdt:P585 ?pointInTime }}
                  OPTIONAL
                    {{ ?item  wdt:P569  ?dateOfBirth }}
                  OPTIONAL
                    {{ ?item  wdt:P570  ?dateOfDeath }}
                  OPTIONAL
                    {{ ?item  wdt:P21 ?gender }}
                  OPTIONAL
                    {{ ?item  wdt:P106 ?occupation }}
                  OPTIONAL
                    {{ ?item  wdt:P172 ?ethnicity }}
                  OPTIONAL
                    {{ ?item  wdt:P140 ?religion }}
                  SERVICE wikibase:label
                    {{ bd:serviceParam
                                wikibase:language  "en"
                    }}
                                  }}
              GROUP BY ?item ?itemLabel ?itemDescription ?instanceOf ?countryOfOrigin ?country ?locatedIn ?location ?countryOfCitizenship ?placeOfBirth ?coordinates ?inception ?startTime ?pointInTime ?dateOfDeath ?gender ?occupation ?ethnicity ?religion
                  """)
            sparql.setReturnFormat(JSON)
            query_result = sparql.query().convert()
            try:
                metadata = {wikidata_id: query_result["results"]["bindings"][
                    -1]}  # if there are several search results (e.g. "television actor" & "actor", simply take the last in list)
                #wikidata_metadata_list += [metadata]
                jsonl_file.write(metadata)
            except:
                pass
    return None


def get_label_from_url(wikipedia_url, qid_to_label_map={}):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="bench-gap")
    if not wikipedia_url.startswith("http") and wikipedia_url is not None:
        return wikipedia_url, qid_to_label_map
    else:
        try:
            qid = wikipedia_url.split("/")[-1]
        except:
            print("Couldn't split url:", wikipedia_url)
            return None, qid_to_label_map
        if qid not in qid_to_label_map.keys():
            # Only call API if label has not been retrieved before
            search_item = f"{{(wdt:{qid})}}"
            service = """{ bd:serviceParam wikibase:language "en". }"""
            sparql.setQuery(f""" 
                            SELECT  *
                            WHERE
            {{
                            wd:{qid} rdfs:label ?label .
                            FILTER (langMatches( lang(?label), "EN" ) )
            }} LIMIT 1
            """)
            sparql.setReturnFormat(JSON)
            query_result = sparql.query().convert()
            try:
                result_value = query_result["results"]["bindings"][0]["label"]["value"]
            except:
                print(qid, query_result)
                return None, qid_to_label_map

            qid_to_label_map[qid] = result_value
            return result_value, qid_to_label_map
        else:
            return qid_to_label_map[qid], qid_to_label_map


def get_wiki_feature_values_dict(wikidata_metadata_list, output_path):

    wiki_feature_values_dict = {
        "description_texts": {},
        "locations": {},
        "times": {},
        "genders": {},
        "instance_of": {},
        "coordinates": {},
        "occupations": {},
        "ethnicity": {},
        "religion": {},
    }

    qid_to_label_map = {}

    location_identifiers = ["countryOfOrigin",
                            "country",
                            "locatedIn",
                            "location",
                            "countryOfCitizenship",
                            "placeOfBirth"]
    time_identifiers = ["inception",
                        "startTime",
                        "pointInTime",
                        "dateOfBirth",
                        "dateOfDeath"]

    for feature in wiki_feature_values_dict.keys():
        wiki_feature_values_dict[feature] = {"qids": [], "labels": []}

    for entry in tqdm(wikidata_metadata_list):
        qid, metadata = next(iter(entry.items()))
        wiki_feature_values_dict["description_texts"]["qids"] += [metadata["itemLabel"]["value"]]
        label, qid_to_label_map = get_label_from_url(metadata["itemLabel"]["value"], qid_to_label_map)
        wiki_feature_values_dict["description_texts"]["labels"] += [label]

        for loc_relation in location_identifiers:
            if loc_relation in metadata.keys():
                wiki_feature_values_dict["locations"]["qids"] += [metadata[loc_relation]["value"]]
                label, qid_to_label_map = get_label_from_url(metadata[loc_relation]["value"], qid_to_label_map)
                wiki_feature_values_dict["locations"]["labels"] += [label]
        for time_relation in time_identifiers:
            if time_relation in metadata.keys():
                wiki_feature_values_dict["times"]["qids"] += [metadata[time_relation]["value"]]
                if metadata[time_relation]["value"].startswith("http:"):
                    label, qid_to_label_map = get_label_from_url(metadata[time_relation]["value"], qid_to_label_map)
                else:
                    label = metadata[time_relation]["value"]
                wiki_feature_values_dict["times"]["labels"] += [label]
        if "gender" in metadata.keys():
            wiki_feature_values_dict["genders"]["qids"] += [metadata["gender"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["gender"]["value"], qid_to_label_map)
            wiki_feature_values_dict["genders"]["labels"] += [label]
        if "instanceOf" in metadata.keys():
            wiki_feature_values_dict["instance_of"]["qids"] += [metadata["instanceOf"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["instanceOf"]["value"], qid_to_label_map)
            wiki_feature_values_dict["instance_of"]["labels"] += [label]
        if "coordinates" in metadata.keys():
            wiki_feature_values_dict["coordinates"]["qids"] += [metadata["coordinates"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["coordinates"]["value"], qid_to_label_map)
            wiki_feature_values_dict["coordinates"]["labels"] += [label]
        if "occupation" in metadata.keys():
            wiki_feature_values_dict["occupations"]["qids"] += [metadata["occupation"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["occupation"]["value"], qid_to_label_map)
            wiki_feature_values_dict["occupations"]["labels"] += [label]
        if "ethnicity" in metadata.keys():
            wiki_feature_values_dict["ethnicity"]["qids"] += [metadata["ethnicity"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["ethnicity"]["value"], qid_to_label_map)
            wiki_feature_values_dict["ethnicity"]["labels"] += [label]
        if "religion" in metadata.keys():
            wiki_feature_values_dict["religion"]["qids"] += [metadata["religion"]["value"]]
            label, qid_to_label_map = get_label_from_url(metadata["religion"]["value"], qid_to_label_map)
            wiki_feature_values_dict["religion"]["labels"] += [label]

    for feature_name, values_lists in wiki_feature_values_dict.items():
        print(feature_name, "num. items:", len(values_lists["labels"]))

    print("Storing dict to", output_path)
    with open(output_path, 'w') as json_file:
            json.dump(wiki_feature_values_dict, json_file)

    return wiki_feature_values_dict

