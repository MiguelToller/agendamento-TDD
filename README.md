
---

### 1. Motivação e Oportunidade

Atualmente, 22% do tempo das secretárias em clínicas parceiras é gasto resolvendo conflitos de agenda ou renegociando horários que foram marcados fora do turno do médico.

**Números do Problema (Fictícios):**
* **Taxa de erro manual:** 15% dos agendamentos via sistema atual permitem sobreposição acidental.
* **Churn:** Clínicas de médio porte relatam perda de R$ 5.000/mês devido a furos na agenda onde o médico não estava disponível, mas o horário estava "aberto".
* **Oportunidade:** Automatizar a validação de disponibilidade pode reduzir o tempo de marcação em 40% e zerar conflitos de horários.

---

### 2. Requisitos Funcionais (RF)

* **RF01 - Configuração de Grade:** O sistema deve permitir definir o horário de início e fim da jornada de um médico, bem como os seus dias de atendimento na semana.
* **RF02 - Validação de Horário e Dia:** Não deve ser possível agendar um paciente fora do horário de trabalho do médico, nem em dias em que ele não atende (folgas). O sistema também deve bloquear consultas que comecem no turno, mas terminem no dia seguinte (virada da noite).
* **RF03 - Prevenção de Sobreposição:** O sistema deve impedir dois agendamentos no mesmo horário (conflito total ou parcial) para a mesma agenda.
* **RF04 - Duração Fixa:** Cada consulta possui uma duração padrão (ex: 30 minutos) que poderá ser alterada em outra história.
* **RF05 - Gestão de Pacientes:** O sistema deve registrar o agendamento atrelado a uma entidade rica de **Paciente** (com ID único, CPF e telefone), abandonando o uso de tipos primitivos (strings) para identificação.

---

### 3. Critérios de Aceitação

**Cenário 1: Agendamento com sucesso**
* **Dado** que o Médico "Dr. House" atende das 08:00 às 12:00
* **E** não existe nenhum agendamento para às 09:00
* **Quando** eu tentar agendar uma consulta para às 09:00
* **Então** o agendamento deve ser confirmado com sucesso.

**Cenário 2: Erro por fora do horário de atendimento**
* **Dado** que o Médico "Dr. House" atende das 08:00 às 12:00
* **Quando** eu tentar agendar uma consulta para às 14:00
* **Então** o sistema deve rejeitar o agendamento informando que o médico não atende neste horário.

**Cenário 3: Erro por conflito de horário (Sobreposição)**
* **Dado** que a agenda do "Dr. House" já possui uma consulta às 10:00 (duração de 30 min)
* **Quando** eu tentar agendar uma nova consulta às 10:15 para a mesma agenda
* **Então** o sistema deve exibir um erro de "Conflito de Horário".

**Cenário 4: Erro por agendamento em dia de folga**
* **Dado** que o "Dr. House" atende apenas de Segunda, Quarta e Sexta
* **Quando** eu tentar agendar uma consulta para um Sábado
* **Então** o sistema deve rejeitar a requisição informando erro de dia indisponível.

**Cenário 5: Erro por invasão de madrugada (Virada de dia)**
* **Dado** que o "Dr. Coruja" atende até às 23:59
* **Quando** eu tentar agendar uma consulta às 23:45 (com término previsto para as 00:15 do dia seguinte)
* **Então** o sistema deve bloquear o agendamento por ultrapassar o limite do turno.

---

### 4. Diretrizes Técnicas e Regras do Desafio

* **TDD (Test-Driven Development):** É obrigatório o desenvolvimento guiado por testes. O código de produção só deve ser escrito após a existência de um teste que falhe.
* **Modelagem C4:** Recomenda-se o desenho da solução utilizando os níveis de Contexto, Contêineres e Componentes para mapear o fluxo arquitetural.
* **Design by Contract (DbC) e Fail-Fast:** O software deve operar sob contratos claros (pré-condições). Utilize a estratégia fail-fast no topo dos métodos para garantir que dados inválidos não sejam processados.
* **Encapsulamento e SRP (SOLID):** O estado interno dos objetos deve ser protegido (ex: uso de tuplas no lugar de listas abertas). As classes devem possuir responsabilidade única (ex: o Médico delega o controle matemático de tempo para uma entidade própria de **Agenda**).
"""

