# b2bflow – Desafio Estágio Python

Lê contatos do **Supabase** e envia mensagens de WhatsApp via **Z-API**.

---

## Pré-requisitos

- Python 3.11+
- Conta gratuita no [Supabase](https://supabase.com)
- Conta gratuita no [Z-API](https://z-api.io)

---

## Setup da tabela no Supabase

No **SQL Editor** do seu projeto Supabase, execute:

```sql
create table contacts (
  id    bigint generated always as identity primary key,
  name  text not null,
  phone text not null
);

-- Exemplos de contatos
insert into contacts (name, phone) values
  ('Ana Silva',    '5511999990001'),
  ('Bruno Lima',   '5511999990002'),
  ('Carla Santos', '5511999990003');
```

> O campo `phone` deve estar no formato internacional sem `+` ou espaços, ex: `5511999990001`.

---

## Variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

| Variável           | Onde encontrar                                              |
|--------------------|-------------------------------------------------------------|
| `SUPABASE_URL`     | Supabase → Project Settings → API → Project URL            |
| `SUPABASE_KEY`     | Supabase → Project Settings → API → anon/public key        |
| `ZAPI_INSTANCE`    | Z-API → Suas Instâncias → ID da instância                  |
| `ZAPI_TOKEN`       | Z-API → Suas Instâncias → Token                            |
| `ZAPI_CLIENT_TOKEN`| Z-API → Conta → Security → Client-Token                    |
| `MAX_CONTACTS`     | Opcional (padrão `3`). Limite de contatos processados.     |

---

## Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/b2bflow-challenge.git
cd b2bflow-challenge

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# edite o .env com suas credenciais

# 5. Execute
python main.py
```

### Exemplo de saída

```
2025-06-23 10:00:01 [INFO] Buscando contatos no Supabase...
2025-06-23 10:00:02 [INFO] 3 contato(s) encontrado(s).
2025-06-23 10:00:02 [INFO] Enviando mensagem para Ana Silva (5511999990001)...
2025-06-23 10:00:03 [INFO] ✅ Mensagem enviada com sucesso para Ana Silva (5511999990001).
2025-06-23 10:00:03 [INFO] Enviando mensagem para Bruno Lima (5511999990002)...
2025-06-23 10:00:04 [INFO] ✅ Mensagem enviada com sucesso para Bruno Lima (5511999990002).
2025-06-23 10:00:04 [INFO] Enviando mensagem para Carla Santos (5511999990003).
2025-06-23 10:00:05 [INFO] ✅ Mensagem enviada com sucesso para Carla Santos (5511999990003).
2025-06-23 10:00:05 [INFO] Resumo: 3 enviado(s) com sucesso, 0 falha(s).
```

---

## Estrutura do projeto

```
b2bflow-challenge/
├── main.py          # Script principal
├── requirements.txt # Dependências
├── .env.example     # Template de variáveis de ambiente
├── .gitignore
└── README.md
```
