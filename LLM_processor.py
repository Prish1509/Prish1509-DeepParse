from dotenv import load_dotenv
from groq import Groq

# load environment variables from .env file
load_dotenv()

# create a groq client instance
groq = Groq()

# function to classify a log using a large language model
def classify_with_llm(log_msg):
    # prepare the prompt for the llm
    prompt = f'''Classify the log message into one of these categories:
(1) Workflow Error, (2) Deprecation Warning.
If you can't figure out a category, return "Unclassified".
Only return the category name. No preamble.
Log message: {log_msg}'''

    # send the prompt to the llama3 model and get the response
    chat_completion = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    # return the category from the response
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    # test the function with a few example logs
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent did not take action."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the new module."))
    print(classify_with_llm(
        "System reboot initiated by user 12345."))
