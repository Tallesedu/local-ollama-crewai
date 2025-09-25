import os
from langchain_ollama import ChatOllama
from crewai import Agent, Task, Crew, Process,LLM

'BURLAR O OPENAI_API_KEY'
os.environ['OPENAI_API_KEY'] = "NA"

'FORMA ANTIGA (NÃO FUNCIONOU COMIGO)'
""" ollama = ChatOllama(
    model="llama3.1:8b",
    base_url="http://localhost:11434"
) """

'FORMA EM QUE CONSEGUI ALTERAR PARA UTILIZAR OLLAMA COM CREWAI'
ollama=LLM(model="ollama/llama3.1:8b", base_url="http://localhost:11434")

copywriter = Agent(
  role = "Copywriter de Marketing",
  llm = ollama,
  verbose = True,
  goal = "Criar textos curtos, chamativos e persuasivos para uma landing page moderna para o tema: {tema}",
  backstory = "Você é especialista em marketing digital e copywriting para conversão sobre o : {tema}"
)

designer = Agent(
  role = "UI/UX Designer",
  llm = ollama,
  verbose = True,
  goal = "Definir a estrutura e o estilo de uma landing page moderna e tecnológica. Planejar um layout moderno com interações e animações.",
  backstory = "Você é um designer criativo que entende de landing pages minimalistas e responsivas. Você cria wireframes e sugere animações e interações modernas (carrosséis, hover effects, fade-in, parallax, etc.)."
)

developer = Agent(
  role = "Frontend Developer Senior",
  llm = ollama,
  verbose = True,
  goal = "Transformar textos e layout em código React + Tailwind + Framer Motion.",
  backstory = "Você é especialista em criar landing pages modernas e interativas em React. Use Tailwind e Framer Motion para animações suaves."
)

copy_task = Task(
  description = """Crie textos (hero, features, testimonials, CTA, footer) para uma landing page tecnológica e inovadora.
    "Escreva textos para uma landing page de tecnologia que apresente um produto digital inovador sobre o tema: {tema}.
    "A página deve ter: Hero section (headline + subheadline + CTA), seção de features, seção de depoimentos e footer.
    "Entregue em formato estruturado (hero, features, testimonials, footer).""",
  expected_output = "Estrutura textual organizada para a landing page.",
  agent = copywriter
)

design_task = Task(
  description = """Crie o wireframe textual da landing page moderna e tecnológica.
    Use a estrutura textual fornecida pelo copywriter.
    Com base nos textos, crie um wireframe textual detalhado. Sugira interações modernas (hover animations, scroll effects, carrosséis, etc.).
    Inclua organização de seções, hierarquia visual e estilo moderno (minimalista, responsivo, tecnológico).""",
  expected_output = "Wireframe textual com anotações de interatividade e animações.",
  agent = designer
)

dev_task = Task(
  description = """Com base nos textos e no wireframe, gere o código completo em React + Tailwind + Framer Motion.
    "Inclua animações de entrada (fade, slide), hover effects, carrossel de depoimentos, e CTA animado.
    "Estruture em componentes reutilizáveis (Hero.jsx, Features.jsx, Testimonials.jsx, Footer.jsx). 
    "Salve como landing.jsx.""",
  expected_output = "Código React completo salvo em landing.jsx",
  output_file = "landing.jsx",
  agent = developer
)

equipe = Crew(
    agents=[copywriter, designer, developer],
    tasks=[copy_task, design_task, dev_task],
    process= Process.sequential
)

tema = "Landing Pages Modernas"

resultado = equipe.kickoff(inputs={
    'tema': tema
})

print(resultado)