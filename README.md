# Social Bias in Popular Question-Answering Benchmarks
Code for the analyses presented in the paper "Social Bias in Popular Question-Answering Benchmarks".

To replicate our benchmark dataset analyses, you must download the benchmark datasets into a datasets folder. 
You may specify its location in `config.yml`. Afterwards, you can simply run `run_data_extraction.py`. It will 
automatically run the entity linking and retrieval of Wikidata properties. 

The `notebooks` folder contains the notebooks we used to 
- identify popular benchmarks in the PwC corpus
- analyze annotations from the manual paper codings
- analyze and visualize the extracted Wikidata properties

To use the entity linker, please install ReFinED as described here: https://github.com/amazon-science/ReFinED?tab=readme-ov-file. 

The annotation guide/questionnaire used for our benchmark paper analyses can be found in `additional_resources`.
