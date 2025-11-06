import json, os

from src.dataloaders.abstract_loader import BenchDataLoader


class DROPDataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "DROPQA"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.data_dict = self._load_data(os.path.join(data_dir, "drop_dataset_dev.json"))
        self.question_list = self.data_dict["question_list"]
        self.answer_list = self.data_dict["entity_list"]
        self.entity_list = self.data_dict["entity_list"]
        self.match_wiki = True
        self.match_ner = False
        self.link_entities = False
        self.split = "dev"


    def _load_data(self, data_path):
        with open(data_path, 'r') as json_file:
            data = json.load(json_file)
        print("Loaded", len(data), "datapoints")

        question_list = []
        answer_spans = []
        # %%
        for key, value in data.items():
            for qa_pair in value["qa_pairs"]:
                question_list += [qa_pair["question"]]
                if len(qa_pair["answer"]["spans"]) > 0:
                    answer_spans += [span for span in qa_pair["answer"]["spans"]]

        return {"question_list": question_list, "answer_list": answer_spans, "entity_list": answer_spans}

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
