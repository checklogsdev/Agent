# CheckLogs Agent

<div align="center">

![CheckLogs Logo](https://via.placeholder.com/150x150?text=CheckLogs)

**Professional Server Monitoring Made Simple**

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/checklogs/agent)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)

[Website](https://checklogs.dev) • [Documentation](https://checklogs.dev/docs) • [Support](mailto:hey@checklogs.dev)

</div>

---

## 🚀 Quick Start

Get your server monitored in less than 2 minutes:

```bash
# 1. Create installation directory
mkdir -p /opt/checklogs && cd /opt/checklogs

# 2. Download docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/checklogsdev/Agent/main/docker-compose.yml

# 3. Create configuration file
cat > .env << 'EOF'
CHECKLOGS_API_KEY=your_api_key_from_dashboard
CHECKLOGS_API_PORT=your_udp_port_from_dashboard
SERVER_NAME=My Production Server
EOF

# 4. Start the agent
docker-compose up -d

# 5. Check logs
docker-compose logs -f
```

That's it! Your server will appear in the dashboard within 30 seconds.

---

## ✨ Features

- 📊 **Real-time Monitoring** - Track CPU, RAM, disk, and network metrics with 10-second intervals
- 🔔 **Smart Alerts** - Get notified when metrics exceed your defined thresholds
- 📈 **Historical Data** - Analyze performance trends over time
- 🔄 **Process Tracking** - Monitor top processes and detect anomalies
- 🚀 **Lightweight** - Uses less than 5% CPU and 50MB RAM
- 🔒 **Secure** - Unique API keys and dedicated UDP ports per server
- 🌐 **Auto-Discovery** - No IP configuration required - your server IP is automatically detected
- 👥 **Team Collaboration** - Share access with team members and manage permissions

---

## 📋 Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 1.29 or higher
- Active CheckLogs account ([Sign up here](https://checklogs.dev))
- Linux server (Ubuntu, Debian, CentOS, RHEL, etc.)

---

## 📦 Installation

### Step 1: Add Server in Dashboard

1. Log in to your [CheckLogs Dashboard](https://checklogs.dev)
2. Click "Add Server"
3. Copy your **API Key** and **UDP Port**

### Step 2: Install Agent on Your Server

```bash
mkdir -p /opt/checklogs && cd /opt/checklogs

curl -o docker-compose.yml https://raw.githubusercontent.com/checklogsdev/Agent/main/docker-compose.yml

cat > .env << 'EOF'
CHECKLOGS_API_KEY=your_api_key_here
CHECKLOGS_API_PORT=your_udp_port_here
SERVER_NAME=Production Server 01
COLLECT_INTERVAL=10
EOF

docker-compose up -d
```

### Step 3: Verify Installation

```bash
# Check agent status
docker-compose ps

# View logs
docker-compose logs -f

# Should see:
# ✓ Configuration valid
# ✓ Agent started successfully
# 📊 Collecting metrics every 10 seconds
# 📦 Sent 1234 bytes to api.checklogs.dev:9876
```

---

## ⚙️ Configuration

All configuration is done via environment variables in the `.env` file:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CHECKLOGS_API_KEY` | Your unique API key (from dashboard) | `a1b2c3d4e5f6...` |
| `CHECKLOGS_API_PORT` | Your assigned UDP port (from dashboard) | `9876` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_NAME` | Display name for your server | `My Server` |
| `COLLECT_INTERVAL` | Collection interval in seconds | `10` |
| `COLLECT_CPU` | Enable CPU metrics | `true` |
| `COLLECT_RAM` | Enable RAM metrics | `true` |
| `COLLECT_DISK` | Enable disk metrics | `true` |
| `COLLECT_LOAD` | Enable load average metrics | `true` |
| `COLLECT_PROCESSES` | Enable process tracking | `true` |
| `TOP_PROCESSES_COUNT` | Number of top processes to track | `10` |
| `LOG_LEVEL` | Logging level (debug/info/warning/error) | `info` |

### Example Configuration

```bash
# Required
CHECKLOGS_API_KEY=a1b2c3d4e5f6789...
CHECKLOGS_API_PORT=9876

# Optional
SERVER_NAME=Web Server 01
COLLECT_INTERVAL=10
COLLECT_CPU=true
COLLECT_RAM=true
COLLECT_DISK=true
COLLECT_LOAD=true
COLLECT_PROCESSES=true
TOP_PROCESSES_COUNT=10
LOG_LEVEL=info
```

---

## 📊 Collected Metrics

### CPU Metrics
- Overall CPU utilization percentage
- User space CPU time
- Kernel space CPU time
- I/O wait time

### Memory Metrics
- Total RAM installed
- Used RAM
- Available RAM
- Cached/buffered memory
- Swap usage

### Disk Metrics
- Total disk capacity (per partition)
- Used disk space
- Disk utilization percentage
- Inode usage

### Load Average
- 1-minute load average
- 5-minute load average
- 15-minute load average

### Process Metrics
- Top processes by CPU usage
- Top processes by memory usage
- Process status and owner
- Command line information

### System Information
- Uptime
- Boot time
- Hostname
- OS information

---

## 🔧 Management Commands

```bash
# Start agent
docker-compose up -d

# Stop agent
docker-compose down

# Restart agent
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Update agent to latest version
docker-compose pull
docker-compose up -d

# Remove agent and data
docker-compose down -v
```

---

## 🛠️ Troubleshooting

### Agent Not Connecting

**Symptoms:** Server shows as "offline" in dashboard

```bash
# Check agent status
docker-compose ps

# View detailed logs
docker-compose logs -f

# Verify configuration
cat .env | grep CHECKLOGS

# Test network connectivity
nc -u -v api.checklogs.dev 9876
```

### High Resource Usage

If the agent is consuming too much resources:

1. Increase `COLLECT_INTERVAL` to 30 or 60 seconds
2. Disable unnecessary metrics (set to `false`)
3. Reduce `TOP_PROCESSES_COUNT` to 5

```bash
# Edit .env file
nano .env

# Restart agent
docker-compose restart
```

### Missing Metrics

If certain metrics aren't appearing:

- Ensure the metric is enabled in `.env`
- Check agent logs for errors
- Verify Docker has proper host access (privileged mode is required)

### Common Errors

**"Invalid API Key"**
- Double-check your API key in the `.env` file
- Copy it exactly from the dashboard (64 characters)

**"Connection refused"**
- Check firewall rules
- Ensure outbound UDP traffic is allowed to `api.checklogs.dev`

**"Permission denied"**
- Ensure Docker is running in privileged mode
- Required to access host system metrics

---

## 🔒 Security

- Each server has a **unique 64-character API key**
- Each server gets a **dedicated UDP port** (9876-10875 range)
- Metrics are **validated** against your API key
- Only **team members** can access server data
- No sensitive data is transmitted
- **IP auto-detection** - your server IP is automatically detected from UDP packets

---

## 🏗️ Architecture

```
┌─────────────────┐         UDP          ┌──────────────────┐
│  Your Server    │    (Port 9876+)      │  CheckLogs API   │
│                 │─────────────────────▶│  api.checklogs   │
│  Docker Agent   │   Metrics + API Key  │      .dev        │
│  (checklogs/    │                      │                  │
│   agent:latest) │                      │  - Validates key │
└─────────────────┘                      │  - Stores data   │
        │                                │  - Auto-detects  │
        │ Collects every 10s             │    your IP       │
        ▼                                └──────────────────┘
┌─────────────────┐                              │
│  Host System    │                              │
│  /proc, /sys    │                              ▼
│  Disk, CPU,     │                      ┌──────────────────┐
│  RAM, Processes │                      │  Web Dashboard   │
└─────────────────┘                      │  checklogs.dev   │
                                         │                  │
                                         │  - View metrics  │
                                         │  - Set alerts    │
                                         │  - Manage teams  │
                                         └──────────────────┘
```

---

## 📚 Documentation

For complete documentation, visit [checklogs.dev/docs](https://checklogs.dev/docs)

Topics covered:
- Getting started guide
- Advanced configuration
- Alert setup
- Team management
- API reference
- Best practices
- FAQ

---

## 🤝 Support

Need help? We're here for you!

- 📧 Email: [hey@checklogs.dev](mailto:hey@checklogs.dev)
- 📖 Documentation: [checklogs.dev/docs](https://checklogs.dev/docs)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/checklogsdev/Agent/issues)
- 💬 Feature Requests: [GitHub Discussions](https://github.com/checklogsdev/Agent/discussions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Why CheckLogs?

✅ **No IP Configuration** - Unlike traditional monitoring, you don't configure any IPs  
✅ **2-Minute Setup** - From zero to monitoring in under 2 minutes  
✅ **Lightweight** - Minimal resource footprint on your servers  
✅ **Real-time** - See metrics update live in your dashboard  
✅ **Team-Friendly** - Built for collaboration with role-based access  
✅ **Open Source Agent** - Transparent, auditable code  

---

<div align="center">

**Made by the CheckLogs Team**

[Website](https://checklogs.dev) • [Dashboard](https://panel.checklogs.dev/) • [Docs](https://panel.checklogs.dev/docs)

</div>