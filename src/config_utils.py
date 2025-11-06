import yaml

from src.dataloaders.triviaqa_loader import TriviaQADataLoader
from src.dataloaders.nq_loader import NQDataLoader
from src.dataloaders.boolq_loader import BoolQDataLoader
from src.dataloaders.hotpotqa_loader import HotpotQADataLoader
from src.dataloaders.squad_loader import SQuADDataLoader
from src.dataloaders.quac_loader import QuACDataLoader
from src.dataloaders.drop_loader import DROPDataLoader
from src.dataloaders.coqa_loader import COQADataLoader
from src.dataloaders.webquestions_loader import WebQuestionsDataLoader
from src.dataloaders.strategyqa_loader import StrategyQADataLoader
from src.dataloaders.piqa_loader import PIQADataLoader
from src.dataloaders.winogrande_loader import WinoGrandeDataLoader
from src.dataloaders.copa_loader import COPADataLoader
from src.dataloaders.commonsenseqa_loader import CommonsenseQADataLoader
from src.dataloaders.siqa_loader import SIQADataLoader
from src.dataloaders.hellaswag_loader import HellaSwagDataLoader
from src.dataloaders.truthfulqa_loader import TruthfulQADataLoader
from src.dataloaders.openbookqa_loader import OpenBookQADataLoader
from src.dataloaders.race_loader import RACEDataLoader
from src.dataloaders.scienceqa_loader import ScienceQADataLoader
from src.dataloaders.mmlu_loader import MMLUDataLoader
from src.dataloaders.arc_loader import ARCDataLoader
# from src.dataloaders.gpqa_loader import GPQADataLoader
from src.dataloaders.gsm8k_loader import GSM8KDataLoader


def get_paths():
  with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    print("Config:\n", config)
    return config

def get_benchmark_config():
  # Datasets are assumed to be in the same parent dir
  return [
    # encycl.
    {"name": "TriviaQA", "domain": "encyclopedia", "dataset_path": "TriviaQA/triviaqa-rc/qa", "loader": TriviaQADataLoader},
    {"name": "NaturalQuestions", "domain": "encyclopedia", "dataset_path": "NaturalQuestions", "loader": NQDataLoader},
    {"name": "BoolQ", "domain": "encyclopedia", "dataset_path": "BoolQ", "loader": BoolQDataLoader},
    {"name": "HotpotQA", "domain": "encyclopedia", "dataset_path": "HotpotQA", "loader": HotpotQADataLoader},
    {"name": "SQuAD", "domain": "encyclopedia", "dataset_path": "SQuAD", "loader": SQuADDataLoader},
    {"name": "QuAC", "domain": "encyclopedia", "dataset_path": "QuAC", "loader": QuACDataLoader},
    {"name": "DROP", "domain": "encyclopedia", "dataset_path": "DROP/drop_dataset", "loader": DROPDataLoader},
    {"name": "WebQuestions", "domain": "encyclopedia", "dataset_path": "WebQuestions", "loader": WebQuestionsDataLoader},
    {"name": "StrategyQA", "domain": "encyclopedia", "dataset_path": "StrategyQA", "loader": StrategyQADataLoader},
    {"name": "COQA", "domain": "commonsense", "dataset_path": "COQA", "loader": COQADataLoader},

    # commonsense
    {"name": "PIQA", "domain": "commonsense", "dataset_path": "PIQA/physicaliqa-train-dev", "loader": PIQADataLoader},
    {"name": "WinoGrande", "domain": "commonsense", "dataset_path": "WinoGrande/winogrande_1.1", "loader": WinoGrandeDataLoader},
    {"name": "COPA", "domain": "commonsense", "dataset_path": "COPA", "loader": COPADataLoader},
    {"name": "CommonsenseQA", "domain": "commonsense", "dataset_path": "CommonsenseQA", "loader": CommonsenseQADataLoader},
    {"name": "SIQA", "domain": "commonsense", "dataset_path": "SIQA", "loader": SIQADataLoader},
    {"name": "HellaSwag", "domain": "commonsense", "dataset_path": "HellaSwag", "loader": HellaSwagDataLoader},
    {"name": "TruthfulQA", "domain": "commonsense", "dataset_path": "TruthfulQA", "loader": TruthfulQADataLoader},

    # # school/science
    {"name": "OpenBookQA", "domain": "school and science", "dataset_path": "OpenBookQA/OpenBookQA-V1-Sep2018/Data/Main", "loader": OpenBookQADataLoader},
    {"name": "RACE", "domain": "school and science", "dataset_path": "RACE", "loader": RACEDataLoader},
    {"name": "ScienceQA", "domain": "school and science", "dataset_path": "ScienceQA", "loader": ScienceQADataLoader},
    # #{"name": "BioASQ", "domain": "school and science", "dataset_path": "", "loader": None},
    {"name": "MMLU", "domain": "school and science", "dataset_path": "MMLU", "loader": MMLUDataLoader},
    # #{"name": "MMMU", "domain": "school and science", "dataset_path": "", "loader": None},
    #s{"name": "GPQA", "domain": "school and science", "dataset_path": "GPQA/dataset", "loader": GPQADataLoader},
    {"name": "ARC", "domain": "school and science", "dataset_path": "ARC", "loader": ARCDataLoader},
    {"name": "GSM8K", "domain": "school and science", "dataset_path": "", "loader": GSM8KDataLoader},
    #{"name": "MATH", "domain": "school and science", "dataset_path": "", "loader": None},

    # misc
    #{"name": "OKVQA", "domain": "mulitmodal", "dataset_path": "", "loader": None},
    #{"name": "TextVQA", "domain": "mulitmodal", "dataset_path": "", "loader": None},
  ]
