# HalAi

![Docker](https://img.shields.io/badge/Docker-Desktop-blue?logo=docker)
![n8n](https://img.shields.io/badge/n8n-Automation-orange?logo=n8n)
![License](https://img.shields.io/badge/license-MIT-green)

HalAi è un ambiente **open-source** che combina **n8n** (automazioni low-code) con moduli di **AI generativa** (testo, immagini, audio, video).  
Può essere eseguito **in locale su Windows** tramite Docker Desktop (con WSL2).

---

## 🚀 Funzionalità
- **n8n** con database PostgreSQL e queue mode (Redis + worker).
- **Traefik** per reverse proxy e HTTPS (Let’s Encrypt).
- **Ollama + Open WebUI** per LLM locali.
- **ComfyUI [Unverified]** per generazione immagini (Stable Diffusion).
- **Supporto GPU** (NVIDIA) opzionale.
- Struttura modulare per aggiungere modelli AI (testo/audio/video).

---

## 📂 Struttura progetto

```plaintext
HalAi/
 ├─ docker-compose.yml           # Compose principale
 ├─ docker-compose.gpu.yml       # Variante GPU (opzionale)
 ├─ .env                         # Variabili ambiente
 ├─ n8n_data/                    # Stato persistente n8n
 ├─ postgres_data/               # Stato DB PostgreSQL
 ├─ traefik_letsencrypt/         # Certificati Let's Encrypt
 ├─ models/                      # Modelli AI (LLM, immagini, audio, video)
 ├─ media/                       # Output generati
 └─ workflows/                   # Esempi workflow n8n
