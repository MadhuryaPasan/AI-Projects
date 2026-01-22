import chainlit as cl
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.schema import StrOutputParser
from langchain_classic.schema.runnable import Runnable
from langchain_classic.schema.runnable.config import RunnableConfig
from typing import cast


@cl.on_chat_start
async def on_chat_start():
    model = ChatOllama(
        model="qwen3_nothink:1.7b-q8_0",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


# @cl.on_chat_start
# async def main():
#     # Sending a pdf with the local file path
#     elements = [
#       cl.Pdf(name="pdf1", display="side", path="C:/Users/pkmpp/OneDrive/Documents/Y3S2/TPSM/Lab/lab 1/Lab1/1.pdf", page=1)
#     ]

#     await cl.Message(content="Look at this local pdf1!", elements=elements).send()
@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
