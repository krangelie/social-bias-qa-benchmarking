import os, json

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


class NERMatcher:
    def __init__(self, benchmark_loader, benchmark_data_path):
        self.benchmark_loader = benchmark_loader
        self.output_file = os.path.join(benchmark_data_path, f"{self.benchmark_loader.benchmark_name}_entities_by_type.json")
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer, grouped_entities=True)

    def ner(self):
        ner_results = self.nlp(self.benchmark_loader.get_question_list())
        entities_by_type = {}
        for res in ner_results:
            if len(res) > 0:
                for e in res:
                    if e["entity_group"] not in entities_by_type:
                        entities_by_type[e["entity_group"]] = []
                    entities_by_type[e["entity_group"]] += [e["word"]]
        if self.output_file:
            with open(self.output_file, "w") as f:
                json.dump(entities_by_type, f)
        return entities_by_type