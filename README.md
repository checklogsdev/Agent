# CheckLogs Documentation System

## Overview

The CheckLogs documentation provides comprehensive guides for server monitoring setup and platform usage. Built as a standalone, responsive page matching the panel's design system.

## Access

**URL**: `https://panel.checklogs.dev/docs`

The documentation is accessible without authentication and provides clear, step-by-step instructions for all users.

## Features

### Content Sections

#### 1. Getting Started
Introduction to CheckLogs platform and quick start guide.

#### 2. Installation
Complete agent installation process:
- Prerequisites (Docker 20.10+, Docker Compose 1.29+)
- Step-by-step server setup
- Configuration file creation
- Agent deployment

#### 3. Configuration
Environment variables and settings:
- Required: `CHECKLOGS_API_KEY`, `CHECKLOGS_API_PORT`
- Optional: Collection intervals, metric toggles
- Advanced options

#### 4. Metrics
Detailed explanation of collected data:
- CPU metrics (usage, user, system, I/O wait)
- Memory metrics (total, used, available, cache, swap)
- Disk metrics (usage, inodes)
- Load average (1min, 5min, 15min)
- Process tracking

#### 5. Alerts
Setting up monitoring rules:
- Creating alert rules
- Threshold configuration
- Notification channels
- Alert management

#### 6. Teams & Permissions
Collaboration features:
- Team roles (Owner, Admin, Member, Viewer)
- Permission levels
- Member management
- Access control

#### 7. Integration
How the agent-based system works:
- No manual IP configuration required
- Automatic IP detection from UDP packets
- Fixed API endpoint (`api.checklogs.dev`)
- Port assignment system (9876-10875)

#### 8. Troubleshooting
Common issues and solutions:
- Agent not connecting
- Missing metrics
- High resource usage
- Network connectivity
- Permission errors

#### 9. FAQ
Frequently asked questions about:
- Pricing and plans
- Supported operating systems
- Data retention policies
- Self-hosting options
- Export capabilities

## Localization

Currently French-only.

## Contact

For documentation improvements or corrections:
- Email: contact@checklogs.dev
- GitHub: Issues/Pull Requests
- Dashboard: Support button

## Version History

- v2.0 (Current): Complete rewrite, responsive design
- v1.0: Initial documentation

## Contributing

To contribute to documentation:
1. Fork repository
2. Make changes to `docs.php`
3. Test responsiveness
4. Submit pull request
5. Await review

## License

Documentation content: CC BY 4.0
Code examples: MIT License

---

**Last Updated**: October 2025
**Maintainer**: CheckLogs Team
**Status**: Active Development