import os
import pprint
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.base import ConversationChain
from langchain.chains import LLMChain
from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a SpineAI - A specialized medical assistant with expertise only in spine-related conditions, treatments, and information. You must only respond to spine-related queries even if the same question is asked multiple times. If asked about anything unrelated to the spine, politely decline by stating just this message 'I'm not sure about this topic' . Do not provide speculative or incorrect answers. Only respond if you are confident in your knowledge about the spine. Past Converastions",),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

memory = ConversationBufferWindowMemory(k=8, return_messages=True)  

store = {}


config = {"configurable":{"session_id":"firstchat"}}
def get_history(id:str) -> BaseChatMessageHistory:
    if id not in store:
        store[id] = InMemoryChatMessageHistory() 
    return store[id]


conversation_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

 
def run_chatbot(user_input):
    
    chain =  prompt | llm 
    model_with_memory = RunnableWithMessageHistory(chain,get_history)
    response = model_with_memory.invoke([HumanMessage(content = user_input)],config=config)
    print(response)
    print('\n\n\n\n')
    
    answer = response.content
    memory.save_context({"input": user_input}, {"output": answer})  
    return f"SpineAI: {answer}"


