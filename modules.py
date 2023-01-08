import requests
import markdownify
from conversation import TextDavinci003

class DummyThermostatModule:
    def get_documentation_string(self):
        # dummy implementation
        return '''def get_temperature():
    """Returns the ambient temperature of my house"""

def set_temperature(temp_in_degrees_fahrenheit):
    """Sets the thermostat to specified temperature"""

def schedule_event(event_callable, ISO_8601_timestamp_string)
    """Schedules events in the future."""
'''

    # TODO this carries information about how the prompt is created. Instead it should return a structure with keys
    # corresponding to user input, code to satisfy the request, and an explanation of what the code does.
    def get_example_usage_string(self):
        return '''
TIME: 2022-12-17T10:36:00Z
USER: I want it a little warmer in here.
LOGOS:
I will increase the temperature by 3 degrees.
```python
current_temp = get_temperature()
new_temp = current_temp + 3.0
set_temperature(new_temp)
```

'''

# TODO this implementation is ridiculous. These functions need to be inside their modules.
def get_temperature():
    print('getting temperature - it\'s 72 degrees')
    return 72.0 # dummy value

def set_temperature(temp_in_degrees_fahrenheit):
    print('setting temperature to', temp_in_degrees_fahrenheit)

def schedule_event(event_callable, ISO_8601_timestamp):
    print(f'scheduling event {event_callable} at {ISO_8601_timestamp}')


class WebtextTools:
    def get_documentation_string(self):
        return '''def get_webpage_as_markdown(url):
    """Retrieves the HTML of the webpage at the specified URL, converts it to markdown, and returns the content."""

def summarize_text(text):
    """Summarizes the text using the GPT-3 summarization model."""
'''

    def get_example_usage_string(self):
        return '''
TIME: 2022-12-17T10:36:00Z
USER: Summarize the New York Times homepage for me.
LOGOS:
Here is the summary of the New York Times homepage.
```python
url = 'https://www.nytimes.com/'
markdown = get_webpage_as_markdown(url)
summarize_text(markdown)
```
'''

# TODO this implementation is ridiculous. These functions need to be inside their modules.
def get_webpage_as_markdown(url):
    print(f'getting webpage at {url}')
    resp = requests.get(url)
    if resp.status_code != 200:
        # TODO - needs error handling
        raise Exception(f'Error retrieving webpage. Status code: {resp.status_code}')
    return markdownify.markdownify(resp.text)

text_davinci = TextDavinci003()
def summarize_text(text):
    print('summarizing text:')
    prompt = f'''{text}
------------------------------------
# REQUEST:
Summarize the above text

# RESPONSE:'''
    summary_text = text_davinci.complete(prompt)
    print(summary_text)


class ModuleManager:
    user_prefix = '\nUSER: '

    def load_modules(self):
        self.modules = [DummyThermostatModule(), WebtextTools()]
        pass

    def search_modules(self, request_string):
        "Returns a list of modules that match the request."
        if not self.modules:
            raise Exception('No modules loaded.')
        return self.modules

    def execute_code(self, code):
        "Execute the code and return the result."
        # TODO - this is a raw exec - extremely dangerous. Need create a real implementation
        print('\n>>> # executing RAW code (PWNing your machine):')
        for code_line in code.splitlines():
            print('>>> ' + code_line)
            exec(code_line)

