# 🚀 CheckLogs Agent

Agent de monitoring ultra-léger pour [CheckLogs.dev](https://checklogs.dev)

Surveillez vos serveurs en temps réel : CPU, RAM, Disque, Load, Processus, et plus encore.

---

## ✨ Caractéristiques

- ⚡ **Ultra-léger** : < 20% CPU, < 250 MB RAM
- 🔒 **Sécurisé** : Communication UDP chiffrée
- 🎯 **Précis** : Collecte toutes les 10 secondes
- 🔍 **Intelligent** : Détection automatique d'anomalies
- 🐳 **Simple** : Installation en 1 commande
- 🔄 **Fiable** : Restart automatique en cas d'erreur

---

## 📊 Métriques collectées

### ✅ Par défaut
- **CPU** : Usage global, par cœur, user/system/idle/iowait
- **RAM** : Usage, disponible, cached, buffers
- **Disque** : Usage par partition, IOPS lecture/écriture
- **Load Average** : 1min, 5min, 15min
- **Processus** : Top 10 processus (CPU + RAM)
- **Uptime** : Temps de fonctionnement du serveur

### 🔧 Optionnel
- **Réseau** : Trafic entrant/sortant, connexions actives
- **Température** : CPU, disques (si disponible)

---

## 🚀 Installation rapide

### Méthode 1 : Installation automatique (recommandé)

```bash
curl -sSL https://raw.githubusercontent.com/checklogsdev/dockerfile/main/install.sh | bash
```

### Méthode 2 : Installation manuelle

```bash
# 1. Cloner le repository
git clone https://github.com/checklogsdev/dockerfile.git
cd dockerfile

# 2. Configurer
cp .env.example .env
nano .env  # Remplir les variables

# 3. Démarrer
docker-compose up -d
```

---

## ⚙️ Configuration

Éditez le fichier `.env` :

```bash
# API CheckLogs (fournie lors de l'inscription)
CHECKLOGS_API_HOST=api.checklogs.dev
CHECKLOGS_API_PORT=9876                    # Port UDP unique par serveur
CHECKLOGS_API_KEY=your_api_key_here

# Informations serveur
SERVER_NAME=My Production Server

# Fréquence de collecte (secondes)
COLLECT_INTERVAL=10

# Métriques activées
COLLECT_CPU=true
COLLECT_RAM=true
COLLECT_DISK=true
COLLECT_LOAD=true
COLLECT_PROCESSES=true

# Détection d'anomalies
ANOMALY_DETECTION=true
ANOMALY_THRESHOLD=50
```

---

## 📖 Utilisation

### Avec Make (recommandé)

```bash
make start      # Démarre l'agent
make stop       # Arrête l'agent
make restart    # Redémarre l'agent
make logs       # Affiche les logs en temps réel
make status     # Vérifie le statut
make update     # Met à jour vers la dernière version
make config     # Édite la configuration
```

### Avec Docker Compose

```bash
docker-compose up -d          # Démarrer
docker-compose down           # Arrêter
docker-compose restart        # Redémarrer
docker-compose logs -f        # Logs temps réel
docker-compose pull           # Mettre à jour
```

---

## 🔍 Vérification

### Statut de l'agent

```bash
docker-compose ps
```

### Logs en temps réel

```bash
docker-compose logs -f
```

### Test de connexion

```bash
docker-compose exec agent /app/test-connection
```

---

## 📈 Dashboard

Une fois l'agent installé et connecté, vos métriques sont visibles sur :

👉 **[https://checklogs.dev/dashboard](https://checklogs.dev/dashboard)**

---

## 🔒 Sécurité

- ✅ Communication UDP chiffrée
- ✅ Authentification par clé API unique
- ✅ Accès système en lecture seule
- ✅ Isolation Docker
- ✅ Limites de ressources strictes
- ✅ Pas d'exposition de ports réseau

---

## 🛠️ Architecture

```
┌─────────────────────────────────────┐
│         Votre Serveur               │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    Docker CheckLogs Agent    │  │
│  │                              │  │
│  │  ┌────────────────────────┐ │  │
│  │  │   Collecteur Go        │ │  │
│  │  │   - CPU, RAM, Disk     │ │  │
│  │  │   - Load, Processes    │ │  │
│  │  │   - IOPS, Uptime       │ │  │
│  │  └───────────┬────────────┘ │  │
│  │              │              │  │
│  │              │ UDP          │  │
│  └──────────────┼──────────────┘  │
│                 │                  │
└─────────────────┼──────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  CheckLogs API │
         │ Port UDP dédié │
         └────────────────┘
```

---

## 🐛 Dépannage

### L'agent ne démarre pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier la config
cat .env

# Redémarrer proprement
docker-compose down
docker-compose up -d
```

### Pas de données dans le dashboard

1. Vérifier que l'agent est en ligne : `docker-compose ps`
2. Vérifier les logs : `docker-compose logs -f`
3. Tester la connexion : `docker-compose exec agent /app/test-connection`
4. Vérifier la clé API dans `.env`
5. Vérifier le port UDP (doit être unique par serveur)

### Erreur de permissions

```bash
# Donner les droits à l'utilisateur actuel
sudo chown -R $USER:$USER /opt/checklogs
```

### Mettre à jour l'agent

```bash
docker-compose pull
docker-compose up -d
```

---

## 📦 Configuration avancée

### Changer la fréquence de collecte

```bash
# Dans .env
COLLECT_INTERVAL=5  # Collecte toutes les 5 secondes
```

### Désactiver certaines métriques

```bash
# Dans .env
COLLECT_NETWORK=false    # Désactive la collecte réseau
COLLECT_PROCESSES=false  # Désactive les processus
```

### Ajuster les limites de ressources

Dans `docker-compose.yml` :

```yaml
deploy:
  resources:
    limits:
      cpus: '0.20'      # Max 20% d'1 cœur
      memory: 250M      # Max 250 MB RAM
```

---

## 🔄 Désinstallation

```bash
cd /opt/checklogs
docker-compose down -v
cd ..
sudo rm -rf /opt/checklogs
```

---

## 📞 Support

- 📧 Email : [support@checklogs.dev](mailto:support@checklogs.dev)
- 💬 Discord : [discord.gg/checklogs](https://discord.gg/checklogs)
- 📚 Documentation : [docs.checklogs.dev](https://docs.checklogs.dev)
- 🐛 Issues : [GitHub Issues](https://github.com/checklogsdev/dockerfile/issues)

---

## 📄 Licence

MIT License - voir [LICENSE](LICENSE)

---

## 🌟 Contribuer

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

---

<p align="center">
  Made with ❤️ by <a href="https://checklogs.dev">CheckLogs.dev</a>
</p>
