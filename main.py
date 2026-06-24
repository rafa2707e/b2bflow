import os
import logging
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# ── Configuração de logs ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Carrega variáveis de ambiente ─────────────────────────────────────────────
load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
ZAPI_INSTANCE: str = os.environ["ZAPI_INSTANCE"]
ZAPI_TOKEN: str = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN: str = os.environ["ZAPI_CLIENT_TOKEN"]
MAX_CONTACTS: int = int(os.getenv("MAX_CONTACTS", "3"))


# ── Supabase ──────────────────────────────────────────────────────────────────
def fetch_contacts(supabase: Client) -> list[dict]:
    """Busca até MAX_CONTACTS contatos na tabela 'contacts' do Supabase."""
    logger.info("Buscando contatos no Supabase...")
    response = (
        supabase.table("contacts")
        .select("name, phone")
        .limit(MAX_CONTACTS)
        .execute()
    )
    contacts = response.data
    logger.info(f"{len(contacts)} contato(s) encontrado(s).")
    return contacts


# ── Z-API ─────────────────────────────────────────────────────────────────────
def send_whatsapp_message(phone: str, name: str) -> bool:
    """Envia mensagem de WhatsApp via Z-API para um número."""
    url = (
        f"https://api.z-api.io/instances/{ZAPI_INSTANCE}"
        f"/token/{ZAPI_TOKEN}/send-text"
    )
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }
    message = f"Olá, {name} tudo bem com você?"
    payload = {"phone": phone, "message": message}

    logger.info(f"Enviando mensagem para {name} ({phone})...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        logger.info(f"✅ Mensagem enviada com sucesso para {name} ({phone}).")
        return True
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"❌ Erro HTTP ao enviar para {name} ({phone}): "
            f"{e.response.status_code} – {e.response.text}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de conexão ao enviar para {name} ({phone}): {e}")
    return False


# ── Fluxo principal ───────────────────────────────────────────────────────────
def main() -> None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    contacts = fetch_contacts(supabase)

    if not contacts:
        logger.warning("Nenhum contato encontrado. Encerrando.")
        return

    success, failed = 0, 0
    for contact in contacts:
        name: str = contact.get("name", "").strip()
        phone: str = contact.get("phone", "").strip()

        if not name or not phone:
            logger.warning(f"Contato inválido ignorado: {contact}")
            failed += 1
            continue

        if send_whatsapp_message(phone, name):
            success += 1
        else:
            failed += 1

    logger.info(
        f"Resumo: {success} enviado(s) com sucesso, {failed} falha(s)."
    )


if __name__ == "__main__":
    main()