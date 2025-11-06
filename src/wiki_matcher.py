
import gc

from src.visualization_helpers import *
from src.wiki_helpers import *


class WikidataMatcher:
    def __init__(self,
                 benchmark_loader,
                 benchmark_data_path):
        self.benchmark_name = benchmark_loader.benchmark_name
        # self.question_word_list = benchmark_loader.get_question_word_list()
        # print(self.question_list[:10])
        # self.answer_word_list = benchmark_loader.get_answer_word_list()
        self.benchmark_data_path = benchmark_data_path
        self.wiki_ids_path = os.path.join(self.benchmark_data_path, "wikidata_ids.txt")
        self.wiki_metadata_path = os.path.join(self.benchmark_data_path, "wikidata_metadata.txt")
        self.wiki_feature_distributions = os.path.join(self.benchmark_data_path, "distributions.json")


    def match_wiki(self):
        print("Generating dataset report for", self.benchmark_name)
        if not os.path.exists(self.wiki_ids_path):
            unresolved = get_wikidata_ids_from_entity_names(self.benchmark_loader.get_entity_list(), self.wiki_ids_path)
            print("Unresolved inputs:", unresolved)

        with open(self.wiki_ids_path, 'r') as f:
            wikidata_ids = []
            for entry in f.readlines():
                wikidata_ids += [entry.strip()]


        if not os.path.exists(self.wiki_metadata_path):
            get_wikidata_properties_from_id(wikidata_ids, self.wiki_metadata_path)

        metadata_lists = []
        with open(self.wiki_metadata_path, 'r') as f:
            for entry in f.readlines():
                metadata_lists += [json.loads(entry)]

        gc.collect()

        if os.path.exists(self.wiki_feature_distributions):
            with open(self.wiki_feature_distributions, 'r') as f:
                wiki_feature_values_dict = json.load(f)
        else:
            wiki_feature_values_dict = get_wiki_feature_values_dict(metadata_lists, self.wiki_feature_distributions)

        for feature_name, values_lists in wiki_feature_values_dict.items():
            print(feature_name, "num. items:", len(values_lists["labels"]))
        print("Storing feature frequency dict...")

        gc.collect()

        return wiki_feature_values_dict