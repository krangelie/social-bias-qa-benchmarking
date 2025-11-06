import json, os

from src.dataloaders.abstract_loader import BenchDataLoader


class NQDataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "NaturalQuestions"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data(os.path.join(data_dir, "v1.0-simplified_nq-dev-all.jsonl"))
        self.question_list = self.data_dict["question_list"]
        self.question_tokens = self.data_dict["question_tokens"]
        self.answer_list = None
        self.entity_list = self.data_dict["entity_list"]
        self.match_wiki = True
        self.match_ner = False
        self.link_entities = False
        self.split = "dev"


    def _load_data(self, data_path):
        question_list = []
        entity_list = []
        question_tokens = []
        with open(data_path, 'r') as json_file:
            json_list = list(json_file)
            for json_str in json_list:
                entry = json.loads(json_str)
                question_list += [entry["question_text"]]
                entity_list += [entry["document_url"]]
                question_tokens += [entry["question_tokens"]]
        return {"question_list": question_list, "question_tokens": question_tokens, "entity_list": entity_list}

    def get_number_of_items(self):
        return len(self.question_list)

    def get_question_list(self):
        return self.question_list

    def get_answer_list(self):
        return self.answer_list

    def get_question_word_list(self):
        return self.question_tokens

    def get_answer_word_list(self):
        return None

    def get_entity_list(self):
        return self.entity_list
