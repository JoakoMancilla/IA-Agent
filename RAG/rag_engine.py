from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_core.vectorstores import InMemoryVectorStore

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader

from langchain.tools import tool
from langchain.agents import create_agent

from dotenv import load_dotenv

load_dotenv()
messages = []


# 1️⃣ Modelo LLM
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0

)
print("Acceso a LLM")

# 2️⃣ Modelo de embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# 3️⃣ Vector store (base vectorial)
vector_store = InMemoryVectorStore(embeddings)

# 4️⃣ Cargar PDF
pdf_path = "C:/Joaquin/5.Personal/CV_JoaquinMancilla_2026_Febrero.pdf"
loader = PyPDFLoader(pdf_path)

docs = (loader.load())

# 5️⃣ Splitter para dividir documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

splits = text_splitter.split_documents(docs)

# se crean los embeddings
vector_store.add_documents(splits)

print(f"Enbiddings cargados: {len(splits)}")

# 6️⃣ Tool de retrieval
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""

    print("Acceso a TOOL RETRIEVED")
    retrieved_docs = vector_store.similarity_search(query, k=4)

    serialized = "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}"
        for doc in retrieved_docs
    )

    return serialized, retrieved_docs

tools = [retrieve_context]

prompt = """
You are an assistant that answers questions using ONLY the retrieved context.
If the answer is not in the context, say you don't know.
"""

agent = create_agent(
    model,
    tools,
    system_prompt=prompt
)


def ask(query):

    messages.append({"role": "user", "content": query})

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )



    content = response["messages"][-1].content

    print("\nRespuesta:\n")

    if isinstance(content, list):
        for block in content:
            if block["type"] == "text":
                print(block["text"])
    else:
        print(content)


while True:
    try:
        query = input("\nPregunta: ")

        if query in ['q', 'exit', 'salir']:
            print("\nCerrando RAG... \n")
            break

        ask(query)
    except Exception as e:
        error_msg = str(e)

        if "RESOURCE_EXHAUSTED" in error_msg:
            print("ERROR: Límite de requests alcanzado")
        else:
            print(f"ERROR: {error_msg}")