import json, os
import pandas as pd

from src.dataloaders.abstract_loader import BenchDataLoader


class OpenBookQADataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "OpenBookQA"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data(os.path.join(data_dir, "test.tsv"))
        self.question_list = self.data_dict["question_list"]
        self.answer_list = None
        self.entity_list = None
        self.match_wiki = True
        self.match_ner = True
        self.link_entities = True
        self.split = "test"


    def _load_data(self, data_path):
        data = pd.read_csv(data_path, sep="\t")
        print("Loaded", len(data), "datapoints")
        question_list = data["Complete Question"].to_list()
        return {"question_list": question_list}

    def get_number_of_items(self):
        return len(self.question_list)

    def get_question_list(self):
        return self.question_list

    def get_answer_list(self):
        return self.answer_list

    def get_question_word_list(self):
        question_tokens_list = [question.lower().strip().replace('"', '').replace("'", "").replace("?", "").split() for
                                question in self.question_list]
        corpus = [word for i in question_tokens_list for word in i]
        return corpus

    def get_answer_word_list(self):
        return None

    def get_entity_list(self):
        return self.entity_list
