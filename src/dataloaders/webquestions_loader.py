import pandas as pd

from src.dataloaders.abstract_loader import BenchDataLoader


class WebQuestionsDataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "WebQuestions"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data()
        self.question_list = self.data_dict["question_list"]
        self.answer_list = self.data_dict["answer_list"]
        self.entity_list = self.data_dict["entity_list"]
        self.match_wiki = True
        self.match_ner = False
        self.link_entities = False
        self.split = "test"


    def _load_data(self):
        splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
        data = pd.read_parquet("hf://datasets/Stanford/web_questions/" + splits["test"])
        print("Loaded", len(data), "datapoints")
        question_list = data["question"].to_list()
        answer_list = [a for item in data["answers"] for a in item]

        return {"question_list": question_list, "answer_list": answer_list, "entity_list": answer_list}

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
        answer_tokens_list = [answer.lower().split() for
                              answer in self.answer_list]
        corpus = [word for i in answer_tokens_list for word in i]
        corpus = [c for c in corpus if not c.isnumeric()]
        return corpus

    def get_entity_list(self):
            return self.entity_list
