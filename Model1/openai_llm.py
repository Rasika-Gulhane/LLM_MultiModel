from langchain.chat_models import ChatOpenAI # type: ignore
from langchain.prompts import ChatPromptTemplate # type: ignore
from langserve import add_routes # type: ignore
import os
from constants.sec import open_ai_api_key
import uvicorn # type: ignore
from langchain_community.llms import Ollama # type: ignore
from fastapi import FastAPI # type: ignore



os.environ['OPENAI_API_KEY']= open_ai_api_key
#os.getenv("OPENAI_API_KEY")


#FastAPI app 
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"
)


add_routes(
    app,
    ChatOpenAI(),
    path= '/openai'
)

# Open AI model
model = ChatOpenAI()

# LLM ollama model
llm = Ollama(model ='llama2')



# prompt for essay with openai and poem with llama2
prompt1 = ChatPromptTemplate.from_template(" Write me an essay on {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} for a 5 years child with 100 words")


add_routes(
    app,
    prompt1|model,
    path ="/essay" 

)


add_routes(
    app,
    prompt2|llm,
    path= '/poem'
)




if __name__ == "__main__":
    uvicorn.run(app, host= "localhost", port=8000)