import json, os

from src.dataloaders.abstract_loader import BenchDataLoader


class TriviaQADataLoader(BenchDataLoader):
    def __init__(self, data_dir):
        self.benchmark_name = "TriviaQA"
        print(f"Loading {self.benchmark_name} Dataset ...")
        self.web_dev_json = self._load_data(os.path.join(data_dir, "web-dev.json"))
        self.wiki_dev_json = self._load_data(os.path.join(data_dir, "wikipedia-dev.json"))
        self.web_qa_dict = self._extract_data(self.web_dev_json)
        self.wiki_qa_dict = self._extract_data(self.wiki_dev_json)
        self.question_list = list(set(self.web_qa_dict["question_list"] + self.wiki_qa_dict["question_list"]))
        self.answer_list = list(set(self.web_qa_dict["answer_entities"] + self.wiki_qa_dict["answer_entities"]))
        self.entity_list = self.answer_list
        self.match_wiki = True
        self.match_ner = False
        self.link_entities = False
        self.split = "dev"


    def _load_data(self, data_path):
        with open(data_path, 'r') as json_file:
            data_dict = json.load(json_file)
        return data_dict

    def _extract_data(self, data_dict):
        output_answer_list = []
        output_question_list = []
        unmatched = []
        for i, qa_pair in enumerate(data_dict["Data"]):
            output_question_list += [qa_pair["Question"]]
            try:
                output_answer_list += [qa_pair["Answer"]["MatchedWikiEntityName"]]
            except:
                unmatched += [{i: qa_pair["Question"]}]
        return {"answer_entities": output_answer_list, "question_list": output_question_list, "unmatched": unmatched}

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
