
# Importa módulo para interagir com o sistema operacional
import os 

# Importa a biblioteca Streamlit para a interface web interativa
import streamlit as st

# Importa a classe groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar   
st.set_page_config(
    page_title="Cat AI Coder",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamentos de IA
CUSTOM_PROMPT = """
Você é o "Cat AI Coder", um assistente de IA especialista em programação, com foco principal em Python e C# com aplicações em jogos da Unity. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.


REGRAS DE OPERAÇÃO:
1.  **Foco em Programação e em Ensino**: Responda apenas a perguntas relacionadas a programação, algoritmo, estruturas de dados, bibliotecas ,informações da Unity, estruturas de dados, bibliotecas e frameworks.\
 Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é esclarecer as dúvidas dos iniciantes,\
 porém se eles perguntarem sobre códigos aleatórios de Python responda com um código qualquer do (docs.python.org).

2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de códigos em Python com a sintaxe correta. O código de ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python e oficial da Linguagem C# e Unity \
    (docs.python.org), (https://learn.microsoft.com/pt-br/dotnet/csharp/tour-of-csharp/), (https://learn.microsoft.com/pt-br/dotnet/csharp/),(https://docs.unity.com/en-us), (https://www.tutorialspoint.com/cprogramming/index.htm), (https://learnxinyminutes.com/),\
    (https://devdocs.io/javascript/), (https://www.freecodecamp.org/news/), (https://learn.microsoft.com/pt-br/), (https://developer.mozilla.org/pt-BR/), (https://docs.python.org/3/) ou da Bilioteca em questão.
3.  **Clareza e Precisão**: Use um linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:

    # Define o título da barra lateral
    st.title("🐈Cat AI Coder 1.3")

    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em programação Python e C# com aplicações em jogos da Unity para ajudar iniciantes.")

    # Campo para inserir  a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira usa API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas de programação com Linguagem Python e C#. AI pode cometer erros. Sempre verifique suas respostas.")

    st.markdown("---")
    st.markdown("Feito por Luis Henrique Arvani")
 
    # Título principal do App
    st.title("Poop Company - Cat AI Coder")

    # Subtítulo adicional
    st.title("Assistente Pessoal de Programação Python e C#")

    # Texto auxiliar abaixo do título
    st.caption("Faça sua pergunta sobre a Linguagem Python e C# e obtenha código, explicações e referências.")

    # Inicializa o histórico de mensagens na sessão, caso ainda não exista
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe todas as mensagens anteriores armazenadas no estado de sessão
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
cliente = None

# Verifica se o usuário forneceu a chave Api do Groq
if groq_api_key:

    try:

          # Cria cliente Groq com a chave de API fornecida
          cliente = Groq(api_key = groq_api_key)

    except Exception as e:

            # Exibe erro caso haja problema ao inicializar cliente
            st.error(f"Erro ao inicializar o cliente Groq: {e}")
            st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida sobre Python ou C#?"):

    # Se não houver cliente válido, mostra aviso e para a execução
    if not cliente:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    with st.chat_message("user"):
         st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):

        with st.spinner("Analisando sua pergunta..."):

            try:
                # Faz a chamada para a API
                chat_completion = cliente.chat.completions.create(
                    messages = messages_for_api,
                    model = "llama-3.3-70b-versatile",
                    temperature = 0.7,
                    max_tokens = 2048,
                )

                cat_ai_resposta = chat_completion.choices[0].message.content
                st.markdown(cat_ai_resposta)

                # Salva a resposta da IA no histórico
                st.session_state.messages.append({"role": "assistant", "content": cat_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq:  {e}")

# Rodapé HTML corrigido
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Cat AI Coder - Poop Company</p>
    </div>
    """,
    unsafe_allow_html=True
)


# Obrigado DSA


