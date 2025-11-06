import json, os

from src.dataloaders.abstract_loader import BenchDataLoader


class HellaSwagDataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "HellaSwag"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data(os.path.join(data_dir, "hellaswag_test.jsonl"))
        self.question_list = self.data_dict["question_list"]
        self.answer_list = None
        self.entity_list = None
        self.match_wiki = True
        self.match_ner = True
        self.link_entities = True
        self.split = "dev"


    def _load_data(self, data_path):
        with open(data_path, 'r') as json_file:
            data = list(json_file)
        print("Loaded", len(data), "datapoints")
        question_list = [json.loads(item)["ctx_a"] for item in data]
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
