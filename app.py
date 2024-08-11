from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from models.quiz_card import QuizCard
from datetime import datetime

def get_user_date_input():
    user_input = input("Enter the date (YYYY-MM-DD):")
    try:
        user_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        return user_date
    except ValueError:
        print("Invalid date format.  Please enter the date in YYYY-MM-DD format.")
        return get_user_date_input()
    
def check_date_answer(correct_date, user_date):
    if correct_date == user_date:
        print("Congratulations!  You got the correct date!")
    else:
        days_off = abs((correct_date - user_date).days)
        print(f"You are off by {days_off} day(s).  The correct date was {correct_date.strftime(('%Y-%m-%d'))}")

def get_llm_request(parser):
    system_prompt = SystemMessagePromptTemplate.from_template("""You are a quiz show content creator that creates a trivia question, and answer. 
                                                            The answer to all questions is a date in the format of YYYY-MM-DD, and the topic of 
                                                            the question is supplied by the human.  This is a game so be creative and don't keep 
                                                            giving the same question.""")

    human_prompt = HumanMessagePromptTemplate.from_template("{topic}\n{format_instructions}")

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    return chat_prompt.format_prompt(topic="Canadian History", format_instructions=parser.get_format_instructions()).to_messages()

def get_card(request, parser):
    model = ChatOpenAI(temperature=0.7)

    result = model.invoke(request)

    return parser.parse(result.content)

def main():
    parser = PydanticOutputParser(pydantic_object=QuizCard)

    request = get_llm_request(parser)

    card = get_card(request, parser)

    print(card.question)

    correct_date = card.answer
    user_date = get_user_date_input()

    check_date_answer(correct_date, user_date)

if __name__ == '__main__':
    main()