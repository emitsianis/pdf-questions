from langchain.chat_models import ChatOpenAI

from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.models import ChatArgs
from app.chat.score import random_component_by_score
from app.chat.vector_stores import retriever_map
from app.web.api import get_conversation_components, set_conversation_components


def select_component(
        component_type, component_map, chat_args
):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)

    print(f"Selected components: llm={llm_name}, memory={memory_name}, retriever={retriever_name}")

    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        memory=memory_name,
        retriever=retriever_name,
    )

    condense_question_llm = ChatOpenAI(streaming=False)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata,
    )
