from abc import ABC, abstractmethod


class BenchDataLoader(ABC):
    #@property
    #@abstractmethod
    #def name(self):
    #    pass#
    #
    # @property
    # @abstractmethod
    # def wikidata_related(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def data_path(self):
    #     pass

    @abstractmethod
    def get_number_of_items(self):
        pass

    @abstractmethod
    def get_question_list(self):
        pass

    @abstractmethod
    def get_answer_list(self):
        pass

    @abstractmethod
    def get_entity_list(self):
        pass
    #
    @abstractmethod
    def get_question_word_list(self):
        pass

    @abstractmethod
    def get_answer_word_list(self):
        pass


