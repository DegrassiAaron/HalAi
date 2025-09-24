# HalAi

![Docker](https://img.shields.io/badge/Docker-Desktop-blue?logo=docker)
![n8n](https://img.shields.io/badge/n8n-Automation-orange?logo=n8n)
![License](https://img.shields.io/badge/license-MIT-green)

HalAi è un ambiente **open-source** che combina **n8n** (automazioni low-code) con moduli di **AI generativa** (testo, immagini, audio, video).
Può essere eseguito **in locale su Windows** tramite Docker Desktop (con WSL2) oppure su qualsiasi host Linux compatibile con Docker Engine.

---

## 🚀 Funzionalità
- **n8n** con database PostgreSQL e queue mode (Redis + worker dedicato).
- **Traefik** per reverse proxy, HTTPS automatico (Let’s Encrypt) e routing per sottodomini.
- **Ollama + Open WebUI** per orchestrare e utilizzare LLM locali.
- **ComfyUI [Unverified]** per generazione immagini (Stable Diffusion).
- **Supporto GPU** (NVIDIA) opzionale tramite file Compose dedicato.
- Struttura modulare per aggiungere modelli AI (testo/audio/video) e workflow personalizzati.

---

## 🧱 Architettura dei servizi
| Servizio      | Ruolo principale | Note |
|---------------|-----------------|------|
| Traefik       | Reverse proxy con HTTPS automatico | Espone interfacce web dei servizi sui domini configurati |
| PostgreSQL    | Database transazionale per n8n | Dati persistenti su volume locale |
| Redis         | Backend queue per esecuzioni n8n | Necessario per il queue mode |
| n8n           | Interfaccia principale e API | Accessibile via Traefik sul dominio principale |
| n8n-worker    | Esecutore job asincroni | Gestisce carichi in background tramite Redis |
| Ollama        | Runtime per modelli linguistici locali | Esposto anche sulla porta 11434 per uso diretto |
| Open WebUI    | Interfaccia web per Ollama | Disponibile su sottodominio dedicato |
| ComfyUI       | Pipeline di generazione immagini | Non ufficialmente verificata, uso opzionale |

---

## 📂 Struttura progetto

```plaintext
HalAi/
 ├─ docker-compose.yml           # Compose principale
 ├─ docker-compose.gpu.yml       # Variante GPU (opzionale)
 ├─ .env.example                 # Variabili ambiente (creare .env da questo file)
 ├─ .gitignore                   # Regole di esclusione
 ├─ n8n_data/                    # Stato persistente n8n
 ├─ postgres_data/               # Stato DB PostgreSQL
 ├─ traefik_letsencrypt/         # Certificati Let's Encrypt
 ├─ models/                      # Modelli AI (LLM, immagini, audio, video)
 │   ├─ ollama/                  # Cache modelli Ollama
 │   └─ comfyui/                 # Cache modelli ComfyUI
 ├─ media/                       # Output generati (immagini/audio/video)
 ├─ openwebui_data/              # Dati persistenti Open WebUI
 └─ workflows/                   # Workflow n8n esportati
```

Tutte le cartelle persistenti contengono un file `.gitkeep` per mantenere la struttura nel repository, ma vengono escluse dai commit grazie al `.gitignore`.

---

## ⚙️ Prerequisiti
- **Docker Desktop** (Windows/macOS) o **Docker Engine** (Linux) aggiornato.
- Supporto **WSL2** attivo su Windows.
- Porta **80/443** libere per Traefik.
- (Opzionale) Driver **NVIDIA Container Toolkit** installato per usare la GPU.

---

## 🏁 Avvio rapido
1. Clonare il repository e posizionarsi nella cartella principale.
2. Copiare il file di esempio delle variabili ambiente:
   ```bash
   cp .env.example .env
   ```
3. Aggiornare `.env` con i domini, le credenziali e le chiavi desiderate.
4. Costruire l'immagine personalizzata di ComfyUI (necessario al primo avvio, altrimenti Docker tenterà di scaricare un'immagine inesistente `halai-comfyui`):
   ```bash
   docker compose build comfyui
   ```
5. Avviare l'infrastruttura base:
   ```bash
   docker compose up -d
   ```
6. (Opzionale) Abilitare GPU con file di override:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
   ```
7. Creare record DNS locali (es. tramite file `hosts`) puntando i domini configurati all'host Docker.

Traefik genererà automaticamente certificati Let's Encrypt per i domini pubblicamente raggiungibili. In ambienti locali è possibile utilizzare certificati self-signed o disabilitare l'HTTPS modificando le variabili d'ambiente di Traefik.

---

## 🔐 Sicurezza e configurazione
- **Credenziali n8n**: abilitare la basic auth e sostituire tutte le chiavi di default nel file `.env`.
- **Traefik dashboard**: espone l'interfaccia su `https://traefik.<dominio>`. Valutare l'aggiunta di autenticazione (basic auth o IP allowlist) tramite middleware Traefik.
- **Redis/PostgreSQL**: modificare password predefinite ed eventualmente restringere l'accesso alle sole reti interne Docker.
- **Backup**: eseguire backup periodici delle cartelle `n8n_data`, `postgres_data`, `openwebui_data`, `traefik_letsencrypt`.

---

## 🧩 Estensioni
- Aggiungere nuovi moduli AI creando ulteriori servizi e montando cartelle dedicate sotto `models/`.
- Integrare webhook o API esterne definendo i relativi workflow all'interno della cartella `workflows/`.
- Automatizzare la gestione dell'infrastruttura con script personalizzati (`Makefile`, `Ansible`, ecc.).

---

## 🛠️ Manutenzione
- Aggiornare i servizi eseguendo `docker compose pull` seguito da `docker compose up -d`.
- Monitorare i log con `docker compose logs -f <nome-servizio>`.
- In caso di errori Traefik sui certificati, eliminare `traefik_letsencrypt/acme.json` (verrà rigenerato) e riavviare.
- Il container di ComfyUI viene costruito localmente a partire dal repository ufficiale (vedi `docker/comfyui/`). È possibile
  selezionare un branch o tag specifico impostando la variabile `COMFYUI_GIT_REF` nel file `.env`.

---

## 📜 Licenza
Distribuito con licenza [MIT](LICENSE).
