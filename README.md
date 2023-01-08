# ask-godfrey
the proto chuck

## why "Godfrey"?
So many good reasons:
1. Because the name Chuck was taken.
2. Because I found Godfrey [in an alphabetical list of Butler names](https://kidadl.com/baby-names/inspiration/brilliant-butler-names-for-your-characters).
3. Because I think that if my AI personal assistant ever had a real voice, it should sound like Gilbert Gottfried.
4. Oh wait... those names are spelled differently.
5. Screw it.

## getting started
- Take a look at example.ipynb, and then trace it back to see how it works.

## pieces
- conversation.py - The contains the ability to connect to the OpenAI Large Language Models and also track conversations.
- assistant.py - This specializes the conversation so that it functions as an assistant bot.
- modules.py - This is mocked out at this point but it contains a manager of modules which the assistent refers to in order to find the modules that best service the user's request, and extract documentation.