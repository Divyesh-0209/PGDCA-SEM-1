import os, langchain, langchain_core
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

prompt = ChatPromptTemplate([
    ("system", "You are a professional/formal email generator. You will be provided with email purpose/situation, recipitent type, Important details provided by the user, Desired tone. Based on that you  have to generate a formal/very professional email. You have to strictly write it in a professional way."),
    (MessagesPlaceholder(variable_name="history")),
    ("human", "Write an email for '{purpose}' to '{reciever}', including given important details '{details}' in it, in '{tone}' tone.")
])

chat_model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    api_key = api_key
)

SESSION_STORE = {}

def get_session_history(sid):
    if sid not in SESSION_STORE:
        SESSION_STORE[sid] = InMemoryChatMessageHistory()
    return SESSION_STORE[sid]

starting_pipeline = RunnablePassthrough() | prompt | chat_model | StrOutputParser()

checker = ChatPromptTemplate([
    ("system", "You are an email professionality evaluator. You will be given with an email, you have to evaluate the email on the basis of Grammar, Clarity, Tone, Professionalism, Completeness, Appropriate subject line. You have to strictly answer only in the structured format with fields the 'evaluation' value (HIGH, MEDIUM, LOW), 'identified_issues', can it be directly sent to the reciever without any change ['Change_required' : YES/NO], 'suggestions' and 'improved_email' if changed, then provide the improved version of the email."),
    ("human", "Evaluate this email '{email}'.")
])

def print_email(data):
    print("EMAIL:\n",data['email'])
    return data

checking_pipeline = checker | chat_model | StrOutputParser()

statful_prompt = ChatPromptTemplate([
    ("system", "You are an helper AI. You have to take the recent email from the chat history and do changes in it according to user's current prompt. You have to read and understand the history very carefully and precisely and work/talk only regarding tha email with the user. Strictly avoid other topics in the conversation even if the user try to do so."),
    (MessagesPlaceholder(variable_name="history")),
    ("human", "{input}")
])

stateful_pipeline = RunnablePassthrough() | statful_prompt | chat_model | StrOutputParser()

try:
    my_config={'configurable': {'session_id':"div123"}}

    while True:
        print()
        if my_config["configurable"]["session_id"] not in SESSION_STORE:
            
            stateful_chatbot = RunnableWithMessageHistory(
                starting_pipeline,
                get_session_history,
                input_messages_key="purpose", # Saves the intent
                history_messages_key="history"
            )

            result = stateful_chatbot.invoke({"purpose": input("Enter the purpose of the email: "), "reciever": input("To: "), "details": input("Enter important details to add in email, if any: "), "tone": input("Enter the tone of the email: ")},
                config=my_config)

            print("Email:\n",result)

            evaluation = checking_pipeline.invoke({
                "email" : result
            })

            print("\n Evaluation:\n",evaluation)
        else:
            
            stateful_chatbot = RunnableWithMessageHistory(
                stateful_pipeline,
                get_session_history,
                input_messages_key="input",
                history_messages_key="history"
            )

            prompt = input("\nUser: ").strip()

            if prompt == "" or not prompt:
                raise Exception("Invalid query! try again.")
            else:
                if prompt.lower() == "exit":
                    break
                else:
                    res = stateful_chatbot.invoke({"input": prompt},
                        config=my_config)
                    print("AI:",res)
            
except Exception as e:
    print("ERROR:",e)
