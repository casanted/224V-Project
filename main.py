
import openai

"""
Simple format:
MovieBot: Hey, let's talk about movies! What's your favorite movie?
User: Good question. I like...
MovieBot: Great! ...
"""

openai.api_key = "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"

class SimpleDialog:
    def __init__(self, max_turns, user_name="User", bot_starter=""):
        self.max_turns = max_turns
        self.dialog_text = ""
        self.feed_in_buffer = []
        self.user_name = user_name
        if bot_starter:
            self.dialog_text = "MovieBot: "+bot_starter
            self.feed_in_buffer.append(self.dialog_text)

    def getPrompt(self, user_input, use_history=True):
        return "\n".join(self.feed_in_buffer)+"\n{}: {}\nMovieBot:".format(self.user_name, user_input)

    def append_to_buffer(self, new_content):
        self.feed_in_buffer += new_content
        self.feed_in_buffer = self.feed_in_buffer[-self.max_turns:]
        self.dialog_text += "".join(new_content)

    def getHistory(self):
        return self.dialog_text


def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    return response["choices"][0]["text"]


def create_profile(profile, conversation_history):
    pre_prompt = open("profile_prompt.txt", "r")
    prompt_str = pre_prompt.read()
    pre_prompt.close()
    new_str = f"Current query: {profile}\n" \
              f"New conversation: \n" \
              f"{conversation_history}\nUpdated query:"
    result_prompt = prompt_str + new_str
    return result_prompt


def get_response(profile, conversation_history):
    dialogue = open("response_prompt.txt", "r")
    prompt_str = dialogue.read()
    dialogue.close()
    new_str = f">Dialogue history: \n{conversation_history}" \
              f"\n>Current query: {profile}" \
              f"\nResponse:"
    result_prompt = prompt_str + new_str
    return result_prompt


def recommender():
    user_name = "User"
    dialog = SimpleDialog(max_turns=10, user_name=user_name, bot_starter="Hey, let's talk about movies! I can give you a ton of recommendations as the expert in movies! What's your favorite movie?")
    print(dialog.dialog_text)
    profile = "None"
    while(True):
        print(user_name+": ", end="")
        user_input = input()
        #prompt = dialog.getPrompt(user_input)
        dialog.append_to_buffer(["\n", "{}: {}\n".format(user_name, user_input)])
        profile_string = generate_response(create_profile(profile, dialog.getHistory()))
        response = generate_response(get_response(profile_string, dialog.getHistory()))
        print(profile_string)
        profile = profile_string
        print("MovieBot:" + response)
        dialog.append_to_buffer(["MovieBot:{}".format(response)])



if __name__ == '__main__':
    recommender()
