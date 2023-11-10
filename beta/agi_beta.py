import random
import json
from fuzzywuzzy import fuzz
from textwrap import fill
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SelfLearnableChatbot:
    def __init__(self):
        self.memory = {}
        self.default_response = "I'm not sure I understand."
        self.memory_file = "chatbot_memory.json"
        self.load_memory()

    def respond(self, message):
        message = message.lower()
        best_match = None
        best_score = 0

        for stored_message in self.memory:
            score = fuzz.ratio(message, stored_message)
            if score > best_score:
                best_score = score
                best_match = stored_message

        if best_match and best_score >= 75:
            return random.choice(self.memory[best_match])
        else:
            return self.generate_response(message)

    def generate_response(self, message):
        response = None

        for pattern, possible_responses in self.memory.items():
            if pattern in message:
                response = random.choice(possible_responses)
                break

        return response if response else self.default_response

    def learn(self, message, response):
        similar_pattern = self.find_similar_pattern(message)
        if similar_pattern:
            self.memory[similar_pattern].append(response)
        else:
            self.memory[message.lower()] = [response]
        self.save_memory()

    def find_similar_pattern(self, new_pattern):
        for pattern in self.memory:
            if (
                self.calculate_similarity(new_pattern, pattern) > 0.8
            ):  # Adjust similarity threshold
                return pattern
        return None

    def calculate_similarity(self, text1, text2):
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        similarity = cosine_similarity(vectorizer[0], vectorizer[1])[0][0]
        return similarity

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f)

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            pass


def main():
    chatbot = SelfLearnableChatbot()
    print("Chatbot: Hi! How can I help you today?")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        response = chatbot.respond(user_input)

        if response == chatbot.default_response:
            print("Chatbot:", response)
            new_response = input(
                "Chatbot: I don't know the answer. Could you please provide a response? "
            )
            chatbot.learn(user_input, new_response)
        else:
            print("Chatbot:", fill(response, width=70))


if __name__ == "__main__":
    main()
