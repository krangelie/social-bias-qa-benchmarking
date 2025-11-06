import json, os

from src.dataloaders.abstract_loader import BenchDataLoader


class SQuADDataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "SQuAD"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data(os.path.join(data_dir, "dev-v1.1.json"))
        self.question_list = self.data_dict["question_list"]
        self.answer_list = self.data_dict["answer_list"]
        self.entity_list = self.data_dict["entity_list"]
        self.match_wiki = True
        self.match_ner = False
        self.link_entities = False
        self.split = "dev"


    def _load_data(self, data_path):
        with open(data_path, 'r') as json_file:
            data = json.load(json_file)
        print("Loaded", len(data), "datapoints")

        title_list = []
        question_list = []
        answer_list = []
        for entry in data["data"]:
            title_list += [entry["title"]]
            for paragraph in entry["paragraphs"]:
                for qa in paragraph["qas"]:
                    question_list += [qa["question"]]
                    try:
                        answer_list += [qa["answers"][0]["text"]]
                    except:
                        continue

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
        corpus = [c for c in corpus if not c.isnumeric()
]
        return corpus

    def get_entity_list(self):
        return self.entity_list
