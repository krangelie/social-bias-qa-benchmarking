import os
import json
import gc
import argpase

from src.config_utils import get_paths, get_benchmark_config
from src.wiki_matcher import WikidataMatcher
from src.ner_matcher import NERMatcher
from src.entity_linker import EntityLinker



def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "extract_questions", type=bool, default=False,
                        help="Extract questions from datasets and store externally.")
    parser.add_argument("run_ner", type=bool, default=False,
                        help="Run named entity recognition on questions.")
    parser.add_argument("run_el", type=bool, default=False,
                        help="Run entity linking on questions.")
    parser.add_argument("run_wiki", type=bool, default=False,
                        help="Match entity mentions to Wikidata entities and extract metadata.")
    args = parser.parse_args()
    paths = get_paths()
    datasets_dir  = paths["dataset_path"]
    question_lists_dir = paths["question_path"]
    property_dicts_dir = paths["properties_path"]
    ner_dicts_dir = paths["ner_path"]

    for benchmark in get_benchmark_config():
        name = benchmark["name"]
        path = os.path.join(datasets_dir, benchmark["dataset_path"])
        os.makedirs(path, exist_ok=True)
        print(f"Processing {name}:\n")
        print("Path:", path)
        bench_dataset = benchmark["loader"](path)
        if args.extract_questions:
            question_list = bench_dataset.get_question_list()
            print("Num questions to store", len(question_list))
            question_list_txt = os.path.join(question_lists_dir, f"{name}_questions.txt")
            benchmark_metadata = os.path.join(question_lists_dir, "benchmark_metadata.jsonl")
            metadata_dict = {"bench_name": name,
                             "num_questions": len(question_list),
                             "split": bench_dataset.split}

            if not os.path.exists(question_list_txt):
                os.makedirs(question_lists_dir, exist_ok=True)
                with open(question_list_txt, 'w') as f:
                    f.write("\n".join(question_list))
                mode = 'w' if not os.path.exists(benchmark_metadata) else 'a'
                with open(benchmark_metadata, mode) as f:
                    f.write(json.dumps(metadata_dict) + "\n")
            else:
                print("Question list already exists")

        if bench_dataset.match_ner:
            if not os.path.exists(os.path.join(ner_dicts_dir, f"{name}_entities_by_type.json")):
                os.makedirs(ner_dicts_dir, exist_ok=True)
                ner_matcher = NERMatcher(bench_dataset, ner_dicts_dir)
                _ = ner_matcher.ner()
        if args.run_ner and bench_dataset.match_ner:
            ner_matcher = NERMatcher(bench_dataset, path)
            _ = ner_matcher.ner()

        if args.run_el and bench_dataset.link_entities:
            entity_linker = EntityLinker(bench_dataset,path)
            _ = entity_linker.el()

        if args.run_wiki and bench_dataset.match_wiki:
            wiki_matcher = WikidataMatcher(bench_dataset, path)
            wiki_property_dict = wiki_matcher.match_wiki()
            os.makedirs(property_dicts_dir, exist_ok=True)
            with open(os.path.join(property_dicts_dir, f"{name}_distributions.json"), 'w') as json_file:
                json.dump(wiki_property_dict,json_file)
        gc.collect()


if __name__ == "__main__":
    run()