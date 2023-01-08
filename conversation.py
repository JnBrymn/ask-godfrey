import requests
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
assert OPENAI_API_KEY

class OpenAIModel:
    headers = {'Authorization': 'Bearer ' + OPENAI_API_KEY}

    def __init__(self, temperature=0.5, max_tokens=256, top_p=1, logprobs=5, stop=["\""], frequency_penalty=0, presence_penalty=0):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.logprobs = logprobs
        self.stop = stop
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def complete(self, prompt):
        resp = requests.post(self.url, headers=self.headers, json={
            "prompt": prompt,
            "n": 1,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "logprobs": self.logprobs,
            "stop": self.stop,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        })

        if resp.status_code == 200:
            completion = resp.json()['choices'][0]['text']
        else:
            raise RuntimeError(resp.text)

        return completion


class CodeDavinci002(OpenAIModel):
    url = 'https://api.openai.com/v1/engines/code-davinci-002/completions'


class TextDavinci003(OpenAIModel):
    url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'


class Conversation:
    """A conversation with a chatbot.

    Args:
        open_ai_client: An instance of OpenAI.Client.
        preamble: A string to start the conversation with.
        user_prefix: A string to prefix user input with OR a function that takes user input and returns a string.
        bot_prefix: A string to prefix bot response with.
        stop: A string to stop the conversation with.
        bot_output_processor: A function to process bot response before returning it to the user.
    """

    def __init__(
        self,
        open_ai_client,preamble='',
        user_clause='\n> user: ',
        bot_prefix='\n> bot: ', stop='>',
        bot_output_processor=None,
    ):
        self.open_ai_client = open_ai_client
        self.open_ai_client.stop = stop
        if isinstance(user_clause, str):
            user_clause = lambda x: user_clause + x
        self.user_clause = user_clause
        self.bot_prefix = bot_prefix
        self.stop = stop
        self.bot_output_processor = bot_output_processor or (lambda x: x)
        self.history = preamble

    def say(self, user_input):
        self.history = self.history + self.user_clause(user_input) + self.bot_prefix
        # TODO - handle errors. Right now I'm just letting them bubble up.
        bot_output = self.open_ai_client.complete(self.history)
        self.history = self.history + bot_output
        return self.bot_output_processor(bot_output)

    def print_say(self, user_input):
        print(self.say(user_input))

    def print_history(self):
        print(self.history)

