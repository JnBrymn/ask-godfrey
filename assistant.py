import re
import time

from conversation import Conversation

# TODO update META tag
preamble = '''# LOGOS life automation
LOGOS is an personal assistant AI that converts natural language statements from USER into programmatic scripts that are then executed to fulfill USER's request.

## REQUIRED BEHAVIOR
Below is a conversation between USER an LOGOS. The pattern of the conversations is as follows:
1. In the META tag the relevant API modules are listed and described.
2. The TIME tag prints the USER's current time.
3. The USER tag is the USER's verbal request.
4. The LOGOS tag is the response from LOGOS. LOGOS will then explain what it plans to do using, terse, non-technical English with a friendly feel. LOGOS will first create a python script that will satisfy the user's request.

Additional notes:
- If LOGOS can satisfy the USER request without code (e.g. by simply answering a question), then the LOGOS tag will simply be the answer to the USER's request and no code.
- If LOGOS is unable to satisfy the user's request by using the available modules or by simply answering the question directly, then the LOGOS tag will be a message indicating that LOGOS is unable to satisfy the request.

## CONVERSATION
'''
# LOGOS will first create a python script that will satisfy the user's request. LOGOS will then explain what it just did using simple, terse, non-technical English with a friendly feel.
# LOGOS will then explain what it plans to do using, terse, non-technical English with a friendly feel. LOGOS will first create a python script that will satisfy the user's request.

# TODO - the assistant is a little naive. It doesn't know how to handle multiple requests in a single conversation.
# In practice, the user may have followup questions to corrections. In that case you don't need to re-list the modules UNLESS the user has
# introduced some new information that would require us to introduce new modules. You also probable need some prompt to indicate that that the
# previous completion should be revised
class Assistant:
    completion_re = re.compile(r'\s*([^`]+)\s*?(```python\s*(.+)\s*```\s*)?', re.DOTALL)#TODO this is garbage - rethink

    def __init__(self, open_ai_client, module_manager) -> None:
        self.module_manager = module_manager
        self.conversation = Conversation(
            open_ai_client,
            preamble=preamble,
            user_clause=self._user_clause,
            bot_prefix='',
            stop='\nUSER:',
            bot_output_processor=self._bot_output_processor,
        )

    def _get_timestamp(self):
        return f'TIME: {time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())}'

    def _user_clause(self, request_string):
        "Insert meta data that is useful for executing the request."
        search_modules_result = self.module_manager.search_modules(request_string)
        documentation_string = '''\n\nMETA: The following relevant modules that are available to LOGOS to use in the programmatic scripts:
```python
''' + '\n'.join([module.get_documentation_string() for module in search_modules_result]) + '```\n'
        example_usage_string = '\n'.join([module.get_example_usage_string() for module in search_modules_result])
        timestamp = self._get_timestamp()
        return documentation_string + example_usage_string + timestamp + '\nUSER: ' + request_string + '\nLOGOS:'

    def _bot_output_processor(self, bot_output):
        match = self.completion_re.match(bot_output)
        if not match:
            raise Exception('Unexpected completion format. No match.')
        speech = match.group(1)
        code = match.group(3)
        print(speech)
        if code:
            self.module_manager.execute_code(code)

    def say(self, user_input):
        return self.conversation.say(user_input)

