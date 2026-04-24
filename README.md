## PRD: Módulo de Agendamento Inteligente (MVP)

---

### 1. Motivação e Oportunidade

Atualmente, 22% do tempo das secretárias em clínicas parceiras é gasto resolvendo conflitos de agenda ou renegociando horários que foram marcados fora do turno do médico.

**Números do Problema (Fictícios):**
* **Taxa de erro manual:** 15% dos agendamentos via sistema atual permitem sobreposição acidental.
* **Churn:** Clínicas de médio porte relatam perda de R$ 5.000/mês devido a furos na agenda onde o médico não estava disponível, mas o horário estava "aberto".
* **Oportunidade:** Automatizar a validação de disponibilidade pode reduzir o tempo de marcação em 40% e zerar conflitos de horários.

---

### 2. Requisitos Funcionais (RF)

* **RF01 - Configuração de Grade:** O sistema deve permitir definir o horário de início e fim da jornada de um médico.
* **RF02 - Validação de Horário:** Não deve ser possível agendar um paciente fora do horário de trabalho do médico.
* **RF03 - Prevenção de Sobreposição:** O sistema deve impedir dois agendamentos no mesmo horário para o mesmo médico.
* **RF04 - Duração Fixa:** Cada consulta possui uma duração padrão (ex: 30 minutos) que poderá ser alterada em outra história.

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
* **Então** o sistema deve rejeitar o agendamento informando que o médico não está disponível.

**Cenário 3: Erro por conflito de horário (Sobreposição)**
* **Dado** que o Médico "Dr. House" já possui uma consulta às 10:00
* **Quando** eu tentar agendar uma nova consulta às 10:00 para o mesmo médico
* **Então** o sistema deve exibir um erro de "Conflito de Horário".

---

### 4. Diretrizes Técnicas e Regras do Desafio

* **TDD (Test-Driven Development):** É obrigatório o desenvolvimento guiado por testes. O código de produção só deve ser escrito após a existência de um teste que falhe, garantindo que cada regra de negócio seja validada desde a sua concepção.
* **Modelagem C4:** Recomenda-se o desenho da solução utilizando os níveis de Contexto e Componentes do modelo C4. Isso garante que a estrutura do sistema seja compreendida antes da execução.
* **Design by Contract (DbC):** O software deve operar sob contratos claros de pré-condições, pós-condições e invariantes. Utilize a estratégia fail-fast para garantir que o sistema não processe dados em estado inválido.
* **Encapsulamento e Proteção de Estado:** O estado interno dos objetos deve ser protegido. Utilize propriedades e tipos imutáveis (como tuplas para coleções) para evitar o vazamento de lógica de domínio e garantir que as regras de negócio sejam centralizadas em seus respectivos objetos.
