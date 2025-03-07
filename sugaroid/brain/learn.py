import logging

from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ListTrainer
from nltk import word_tokenize

from sugaroid.sugaroid import SugaroidStatement
from sugaroid.brain.ooo import Emotion
from sugaroid.brain.preprocessors import normalize


class LearnAdapter(LogicAdapter):
    """
    a specific adapter for learning responses
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        normalized = word_tokenize(str(statement).lower())
        try:
            last_type = self.chatbot.globals["history"]["types"][-1]
        except IndexError:
            last_type = False
        logging.info(
            "LearnAdapter: can_process() last_adapter was {}".format(last_type)
        )

        if (
            len(normalized) >= 1
            and normalized[0] == "lleeaarrnn"
            and "not" not in normalized
            and "to" not in normalized
        ):
            return True
        elif self.chatbot.globals["learn"] and (last_type == "LearnAdapter"):
            return True
        else:
            if self.chatbot.globals["learn"]:
                self.chatbot.globals["learn"] = False
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        response = None
        if not self.chatbot.globals["learn"]:
            response = "Enter something you want to teach me. What is the statement that you want me to learn."
            self.chatbot.globals["learn"] = 2
        elif self.chatbot.globals["learn"] == 2:
            response = "What should I respond to the above statement?"
            self.chatbot.globals["learn_last_conversation"].append(str(statement))
            self.chatbot.globals["learn"] -= 1
        elif self.chatbot.globals["learn"] == 1:
            response = "Thanks for teaching me something new. I will try to remember that"
            self.chatbot.globals["learn_last_conversation"].append(str(statement))
            self.chatbot.globals["learn"] -= 1
            list_trainer = ListTrainer(self.chatbot)
            list_trainer.train(self.chatbot.globals["learn_last_conversation"])

        selected_statement = SugaroidStatement(response, chatbot=True)
        selected_statement.confidence = 9
        selected_statement.adapter = "LearnAdapter"
        emotion = Emotion.lol
        selected_statement.emotion = emotion
        return selected_statement
