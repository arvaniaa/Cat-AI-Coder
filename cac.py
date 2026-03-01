# Importa módulo para interagir com o sistema operacional
import os 
# Importa a biblioteca Streamlit para a interface web interativa
import streamlit as st
# Importa a classe groq para se conectar à API da plataforma Groq
from groq import Groq
# Importa para carregar variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv

# Tenta carregar o arquivo .env se ele existir
load_dotenv()

# Configura a página do Streamlit
st.set_page_config(
    page_title="Cat AI Coder",
    page_icon="🐈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define o prompt de sistema (Regras da IA)
CUSTOM_PROMPT = """
Você é o "Cat AI Coder", um assistente de IA especialista em programação, com foco principal em Python, Java e C# com aplicações em jogos da Unity. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.


REGRAS DE OPERAÇÃO:
1.  **Foco em Programação e em Ensino**: Responda apenas a perguntas relacionadas a programação, algoritmo, estruturas de dados, bibliotecas ,informações da Unity, estruturas de dados, bibliotecas e frameworks. Melforias de seu próprios códigos é aceita, mas ser for melhorias viáveis\
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
CUSTOM_PROMPT = """
1. **Estilo e Forma de scripts para jogos da Unity com C#**: Use esses scripts básicos de jogos 2D e 3D da Unity como exemplo para suas criações de script.
* **Script de MovementTopDown2D**:'''csharp
// MovementTopDown2D.cs
// Movimentação top-down 2D usando Rigidbody2D
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class MovementTopDown2D : MonoBehaviour
{
    public float speed = 5f;
    public bool faceMovementDirection = false;

    Rigidbody2D rb;
    Vector2 input;

    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Entrada independente do FixedUpdate para melhor responsividade
        input.x = Input.GetAxisRaw("Horizontal");
        input.y = Input.GetAxisRaw("Vertical");
        input = input.normalized; // evita movimentação mais rápida na diagonal

        if (faceMovementDirection && input.sqrMagnitude > 0.01f)
        {
            float angle = Mathf.Atan2(input.y, input.x) * Mathf.Rad2Deg;
            rb.rotation = angle - 90f; // ajuste conforme sprite
        }
    }

    void FixedUpdate()
    {
        rb.velocity = input * speed;
    }
}
'''
* **Script de ConstantRotate**: '''csharp
// ConstantRotate.cs
// Rotação constante no eixo escolhido
using UnityEngine;

public class ConstantRotate : MonoBehaviour
{
    public Vector3 rotationDegreesPerSecond = new Vector3(0, 0, 90f); // graus por segundo

    void Update()
    {
        transform.Rotate(rotationDegreesPerSecond * Time.deltaTime);
    }
}
'''
* **Script de SimpleFollowAI**:'''csharp
// SimpleFollowAI.cs
// Segue um alvo simples (funciona em 2D ou 3D).
// Em 2D, deixe z fixo; em 3D, segue em XYZ.
using UnityEngine;

public class SimpleFollowAI : MonoBehaviour
{
    public Transform target;
    public float speed = 3f;
    public float stoppingDistance = 0.5f;
    public bool use2D = true; // se true, ignora eixo Z

    void Update()
    {
        if (target == null) return;

        Vector3 targetPos = target.position;
        Vector3 current = transform.position;

        if (use2D) targetPos.z = current.z; // mantém mesma profundidade

        Vector3 dir = (targetPos - current);
        float dist = dir.magnitude;
        if (dist > stoppingDistance)
        {
            Vector3 move = dir.normalized * speed * Time.deltaTime;
            transform.position = current + (move.magnitude > dist ? dir : move);
        }
    }
}
'''
* **Script de Spawner**:'''csharp
// Spawner.cs
// Instancia (cria) objetos (prefab) em posição/rotação dados.
// Possui opção de spawn com offset e respawn por tempo.
using UnityEngine;
using System.Collections;

public class Spawner : MonoBehaviour
{
    public GameObject prefab;
    public Transform spawnPoint; // se nulo usa this.transform
    public Vector3 offset = Vector3.zero;
    public bool spawnOnStart = true;
    public float respawnDelay = 0f; // 0 = não respawna automaticamente

    void Start()
    {
        if (spawnOnStart) Spawn();
        if (respawnDelay > 0f) StartCoroutine(RespawnLoop());
    }

    public GameObject Spawn()
    {
        Transform t = spawnPoint != null ? spawnPoint : transform;
        Vector3 pos = t.position + offset;
        Quaternion rot = t.rotation;
        return Instantiate(prefab, pos, rot);
    }

    IEnumerator RespawnLoop()
    {
        while (true)
        {
            yield return new WaitForSeconds(respawnDelay);
            Spawn();
        }
    }
}
'''
* **Script de RestartLevel**:'''csharp
// RestartLevel.cs
// Reinicia a fase (carrega a cena atual)
using UnityEngine;
using UnityEngine.SceneManagement;

public class RestartLevel : MonoBehaviour
{
    // chama para reiniciar
    public void Restart()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    // Exemplo: reiniciar com tecla R (opcional)
    public bool allowKeyRestart = false;
    public KeyCode restartKey = KeyCode.R;

    void Update()
    {
        if (allowKeyRestart && Input.GetKeyDown(restartKey))
            Restart();
    }
}
'''
* **Script de HealthSystem**:'''csharp
// HealthSystem.cs
// Sistema de vida simples com dano, cura e evento para UI/feedback.
using UnityEngine;
using System;

public class HealthSystem : MonoBehaviour
{
    public int maxHealth = 100;
    public int currentHealth;

    // Evento: assinatura Action<int current, int max>
    public event Action<int, int> OnHealthChanged;
    public event Action OnDeath;
    
    void Awake()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(int amount)
    {
        if (amount <= 0) return;
        currentHealth -= amount;
        currentHealth = Mathf.Clamp(currentHealth, 0, maxHealth);
        OnHealthChanged?.Invoke(currentHealth, maxHealth);
        if (currentHealth == 0) Die();
    }

    public void Heal(int amount)
    {
        if (amount <= 0) return;
        currentHealth += amount;
        currentHealth = Mathf.Clamp(currentHealth, 0, maxHealth);
        OnHealthChanged?.Invoke(currentHealth, maxHealth);
    }

    void Die()
    {
        OnDeath?.Invoke();
        // comportamento padrão: destruir objeto (opcional)
        // Destroy(gameObject);
    }
}
'''
Script de AudioPlayer**:'''csharp
// AudioPlayer.cs
// Controla reprodução de sons via AudioSource
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class AudioPlayer : MonoBehaviour
{
    AudioSource src;

    void Awake()
    {
        src = GetComponent<AudioSource>();
    }

    // Toca um clip (independente do clip atual)
    public void PlayOneShot(AudioClip clip, float volume = 1f)
    {
        if (clip == null) return;
        src.PlayOneShot(clip, volume);
    }

    // Troca o clip do AudioSource e toca (útil para música/loop)
    public void PlayClip(AudioClip clip, bool loop = false)
    {
        if (clip == null) return;
        src.clip = clip;
        src.loop = loop;
        src.Play();
    }

    public void Stop()
    {
        src.Stop();
    }
}
'''
Script de LookAtMouse3D**:'''csharp
// LookAtMouse3D.cs
// Faz o objeto "olhar" para a posição do mouse no mundo (projeta um plano Y).
// Útil para player/torre que segue o cursor no plano XZ.
using UnityEngine;

public class LookAtMouse3D : MonoBehaviour
{
    public Camera mainCamera;
    public float planeY = 0f; // Y do plano onde o objeto olha (ex: chão)
    public bool smooth = true;
    public float smoothSpeed = 10f;
    public bool lockX = false; // manter eixo X fixo
    public bool lockZ = false; // manter eixo Z fixo

    void Awake()
    {
        if (mainCamera == null) mainCamera = Camera.main;
    }

    void Update()
    {
        if (mainCamera == null) return;
        Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);
        // interseção com plano horizontal em Y = planeY
        float t = (planeY - ray.origin.y) / ray.direction.y;
        if (t <= 0) return;
        Vector3 worldPos = ray.origin + ray.direction * t;

        Vector3 target = worldPos;
        Vector3 current = transform.position;
        if (lockX) target.x = current.x;
        if (lockZ) target.z = current.z;

        Vector3 dir = (target - current);
        if (dir.sqrMagnitude < 0.0001f) return;

        Quaternion targetRot = Quaternion.LookRotation(dir.normalized, Vector3.up);
        if (smooth)
            transform.rotation = Quaternion.Lerp(transform.rotation, targetRot, Time.deltaTime * smoothSpeed);
        else
            transform.rotation = targetRot;
    }
}
'''
Script de UIUpdater**:'''csharp
// UIUpdater.cs
// Atualiza texto da UI com valores (suporta UnityEngine.UI.Text e TextMeshProUGUI).
using UnityEngine;
using UnityEngine.UI;
#if TMP_PRESENT
using TMPro;
#endif

public class UIUpdater : MonoBehaviour
{
    public HealthSystem healthSystem; // ligar no inspector ou deixará procurar
    public Text legacyText; // UnityEngine.UI.Text (opcional)
#if TMP_PRESENT
    public TextMeshProUGUI tmpText; // TextMeshPro (opcional)
#endif
    public string format = "HP: {0}/{1}"; // formato de exibição

    void Start()
    {
        if (healthSystem == null)
        {
            healthSystem = FindObjectOfType<HealthSystem>();
        }
        if (healthSystem != null)
        {
            healthSystem.OnHealthChanged += OnHealthChanged;
            // inicializar exibição
            OnHealthChanged(healthSystem.currentHealth, healthSystem.maxHealth);
        }
    }

    void OnDestroy()
    {
        if (healthSystem != null)
            healthSystem.OnHealthChanged -= OnHealthChanged;
    }

    void OnHealthChanged(int current, int max)
    {
        string text = string.Format(format, current, max);
#if TMP_PRESENT
        if (tmpText != null) tmpText.text = text;
#endif
        if (legacyText != null) legacyText.text = text;
    }
}
'''
Script de ColorFeedback**:'''csharp
// ColorFeedback.cs
// Troca cor do SpriteRenderer ou do Material para dar feedback (ex: quando toma dano).
// Usa coroutine para "flash" e retorna cor original.
using UnityEngine;
using System.Collections;

public class ColorFeedback : MonoBehaviour
{
    public Color flashColor = Color.red;
    public float flashDuration = 0.2f;
    public int flashTimes = 2;

    SpriteRenderer spriteRenderer;
    Renderer meshRenderer;
    Color originalColor;
    bool isFlashing = false;

    void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        meshRenderer = GetComponent<Renderer>();
        if (spriteRenderer != null) originalColor = spriteRenderer.color;
        else if (meshRenderer != null) originalColor = meshRenderer.material.color;
    }

    public void Flash()
    {
        if (!isFlashing) StartCoroutine(DoFlash());
    }

    IEnumerator DoFlash()
    {
        if (spriteRenderer == null && meshRenderer == null) yield break;
        isFlashing = true;
        for (int i = 0; i < flashTimes; i++)
        {
            SetColor(flashColor);
            yield return new WaitForSeconds(flashDuration);
            SetColor(originalColor);
            yield return new WaitForSeconds(flashDuration);
        }
        isFlashing = false;
    }

    void SetColor(Color c)
    {
        if (spriteRenderer != null) spriteRenderer.color = c;
        else if (meshRenderer != null)
        {
            // cuidado: modificar instância do material para não alterar todos os objetos que usam o mesmo material
            meshRenderer.material = meshRenderer.material;
            meshRenderer.material.color = c;
        }
    }
}
'''
"""



        
# Conteúdo da barra lateral
with st.sidebar:
    st.title("🐈Cat AI Coder 1.4")
    st.markdown("Um assistente de IA focado em programação Python e C# com aplicações em jogos da Unity.")

    # Busca a chave no arquivo .env ou no sistema. Se não achar, fica vazio.
    api_key_preenchida = os.getenv("GROQ_API_KEY", "")

      # Campo para a chave (já virá preenchido se estiver no .env)
  
   
    

    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em dúvidas de Python e C#. AI pode cometer erros.")
    st.markdown("Feito por Luis Henrique Arvani")

# Título principal do App
st.title("Poop Company - Cat AI Coder")
st.caption("Faça sua pergunta sobre a Linguagem Python e C# e obtenha código, explicações e referências.")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa o cliente Groq
cliente = None

if groq_api_key:
    try:
        cliente = Groq(api_key=groq_api_key)
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()
elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário
if prompt := st.chat_input("Qual sua dúvida sobre Python ou C#?"):
    if not cliente:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara as mensagens para a API
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                chat_completion = cliente.chat.completions.create(
                    messages=messages_for_api,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=2048,
                )

                cat_ai_resposta = chat_completion.choices[0].message.content
                st.markdown(cat_ai_resposta)
                st.session_state.messages.append({"role": "assistant", "content": cat_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

# Rodapé
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Cat AI Coder - Poop Company</p>
    </div>
    """,
    unsafe_allow_html=True
)

#Obrigado DSA












