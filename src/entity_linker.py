import os, json

from refined.inference.processor import Refined


class EntityLinker:
    def __init__(self, benchmark_loader, benchmark_data_path):
        self.benchmark_loader = benchmark_loader
        self.wiki_ids_path = os.path.join(benchmark_data_path, "wikidata_ids.txt")
        self.wiki_entity_names_path = os.path.join(benchmark_data_path,
                                                   f"{self.benchmark_loader.benchmark_name}_entities_by_type.json")
        self.refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers', entity_set="wikipedia")

    def apply_linker(self, text_list):
        docs = self.refined.process_text_batch(text_list)
        return docs

    def get_entities_and_ids(self, docs):
        entities_by_type = {}
        wiki_ids = []

        for doc in docs:
            for span in doc.spans:
                entity_type = span.coarse_mention_type
                if entity_type not in entities_by_type:
                    entities_by_type[entity_type] = []
                if span.date is not None:
                    entities_by_type[entity_type] += [span.date.text]
                elif span.predicted_entity is not None and span.predicted_entity.wikidata_entity_id is not None:
                    wiki_ids += [span.predicted_entity.wikidata_entity_id]
                    entities_by_type[entity_type] += [span.predicted_entity.wikipedia_entity_title]
                else:
                    continue
        return wiki_ids, entities_by_type

    def el(self):
        docs = self.apply_linker(self.benchmark_loader.get_question_list())
        wiki_ids, entities_by_type = self.get_entities_and_ids(docs)
        with open(self.wiki_ids_path, "w") as f:
            for wiki_id in wiki_ids:
                f.write(f"{wiki_id}\n")
        with open(self.wiki_entity_names_path, "w") as f:
            json.dump(entities_by_type, f)
        return None