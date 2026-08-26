# NOVA AI

> **NOVA AI** is a personal AI assistant project focused on building a lightweight, modular, and customizable AI system for desktop use.

## 📦 Installation

### Windows

NOVA is distributed as a normal Windows MSI through GitHub Releases.

1. Open the **Releases** page.
2. Open the latest stable release.
3. Under **Assets**, download `NOVA-AI-<version>-x64.msi`.
4. Run the MSI and install NOVA.

The installer puts the application in `Program Files` and keeps writable user data, memory, and the local AI model in the user's AppData folder so updates do not erase them.

The local Qwen3 GGUF model is downloaded automatically on first use and verified before NOVA loads it. The model is distributed by the `ggml-org/Qwen3-1.7B-GGUF` project on Hugging Face and is listed there under the Apache-2.0 license.

### Updating

NOVA can check for a newer GitHub Release from its system-tray menu. When an update is available, NOVA downloads the new MSI and starts Windows Installer. Your AppData memory and model remain in place, so an application update does not require setting NOVA up from scratch.

---

## 🌌 About NOVA

NOVA is a personal AI assistant being developed with a simple goal:

**Build an AI system that is useful, customizable, lightweight, and fully controlled by its developer.**

The project is designed to evolve gradually from a basic assistant into a complete AI system with its own interface, backend, intelligence layer, tools, and local capabilities.

---

## 🎯 Project Goals

NOVA is being developed around several major goals:

* 🧠 AI intelligence and reasoning
* 💬 Natural conversation
* 🖥️ Desktop integration
* 🌐 Web-based interface
* 🧩 Modular architecture
* ⚡ Lightweight operation
* 🔌 Support for different AI models
* 🗄️ Personal data and memory
* 🛠️ Tool and automation support
* 🔒 Local/private operation where possible
* 🎨 Customizable user interface

---

## 🏗️ Planned Architecture

NOVA is designed as a modular system rather than one giant program.

```text
                         ┌─────────────────┐
                         │    NOVA UI      │
                         │  Web / Desktop  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   NOVA CORE     │
                         │   Controller    │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │ Intelligence│     │   Memory    │     │   Tools     │
       │   Engine    │     │   System    │     │   System    │
       └──────┬──────┘     └─────────────┘     └──────┬──────┘
              │                                        │
              ▼                                        ▼
       ┌─────────────┐                         ┌─────────────┐
       │ AI Models   │                         │ Web/Desktop │
       │ Local/Cloud │                         │ Automation  │
       └─────────────┘                         └─────────────┘
```

### Core Components

| Component               | Purpose                               |
| ----------------------- | ------------------------------------- |
| **NOVA Core**           | Controls the overall assistant        |
| **Intelligence Engine** | Handles AI reasoning and responses    |
| **Model Layer**         | Connects NOVA to different AI models  |
| **Memory System**       | Stores useful information and context |
| **Tool System**         | Allows NOVA to perform actions        |
| **Web Layer**           | Provides the browser-based interface  |
| **Desktop Layer**       | Provides desktop integration          |
| **UI**                  | Handles the user experience           |

---

## 🧠 Intelligence

NOVA is intended to support different AI models instead of being permanently tied to a single model.

Possible model types include:

* Local LLMs
* Cloud AI APIs
* Small specialized models
* Coding models
* Embedding models
* Speech models
* Vision models

The model layer should remain separate from the rest of NOVA so models can be replaced without rebuilding the entire application.

```text
NOVA
 │
 └── Model Manager
      ├── Local Model
      ├── Cloud Model
      ├── Coding Model
      └── Specialized Models
```

---

## 💾 Memory

A planned NOVA memory system can allow the assistant to retain useful context.

Possible memory layers:

```text
Short-Term Memory
        │
        ▼
Conversation Memory
        │
        ▼
Long-Term Memory
        │
        ▼
Personal Knowledge
```

Memory should be modular so it can later use different storage technologies.

---

## 🛠️ Tools

NOVA is intended to eventually interact with tools instead of only generating text.

Potential tools include:

* File management
* Web search
* Calculator
* System information
* Application launching
* Desktop automation
* Code execution
* Database access
* Local services
* Custom developer tools

A tool-based architecture makes it possible to add capabilities without rewriting NOVA's core.

---

## 🖥️ User Interface

The current direction for NOVA's interface is a modern dark-themed UI inspired by contemporary AI applications while maintaining its own design.

Planned characteristics:

* 🌑 Dark interface
* 💬 Chat-based interaction
* ✨ Subtle visual effects
* 🧊 Modern glass-style elements
* 📱 Responsive layout
* ⚡ Lightweight frontend
* 🧩 Modular components

The frontend is planned around:

```text
Frontend
├── HTML
├── CSS
└── JavaScript
```

The backend can communicate with the frontend through an API.

---

## 🔌 Backend

NOVA has experimented with a Python-based backend and Flask.

A simplified architecture is:

```text
Browser / Desktop UI
        │
        ▼
      API
        │
        ▼
   NOVA Backend
        │
   ┌────┼────┐
   ▼    ▼    ▼
 Model Memory Tools
```

The backend is responsible for coordinating NOVA's different systems.

---

## 🐍 Technology Stack

Current and planned technologies include:

### Backend

* Python
* Flask
* REST APIs

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Local LLMs
* Cloud AI APIs
* Model-specific APIs

### Desktop

* Python-based desktop integration
* System automation
* Tray integration

### Development

* Git
* GitHub
* VS Code / lightweight text editors
* Python virtual environments when useful

---

## 📁 Suggested Project Structure

```text
NOVA-AI/
│
├── backend/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── intelligence/
│   ├── memory/
│   ├── models/
│   └── tools/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── desktop/
│   ├── startup.py
│   ├── window.py
│   └── tray.py
│
├── data/
│   └── memory/
│
├── models/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

The exact structure can change as NOVA develops. Prematurely worshipping a folder structure is a surprisingly popular developer hobby.

---

## 🚀 Development Roadmap

### Phase 1 — Foundation

* [x] Create NOVA project
* [x] Basic Python backend
* [x] Basic assistant responses
* [x] Experiment with Flask
* [x] Basic desktop integration
* [x] Tray functionality experiments

### Phase 2 — Web Interface

* [x] Start frontend architecture
* [x] Create main chat interface
* [x] Connect frontend to backend
* [x] Add message history
* [x] Add loading/thinking state
* [x] Improve UI

### Phase 3 — Intelligence

* [x] Model manager
* [x] Local model
* [x] model selection
* [ ] Context management
* [ ] Better reasoning pipeline

### Phase 4 — Memory

* [ ] Conversation memory
* [ ] Persistent memory
* [ ] User preferences
* [ ] Memory search
* [ ] Memory management UI

### Phase 5 — Tools

* [ ] Web tools
* [ ] File tools
* [ ] System tools
* [ ] Coding tools
* [ ] Automation tools
* [ ] Custom tool framework

### Phase 6 — NOVA Desktop

* [ ] Desktop application
* [ ] System tray
* [ ] Global assistant access
* [ ] Desktop automation
* [ ] Lightweight background operation

### Phase 7 — Optimization

* [ ] Reduce RAM usage
* [ ] Reduce CPU usage
* [ ] Optimize model loading
* [ ] Improve startup time
* [ ] Improve reliability
* [ ] Offline functionality

---

## 🔐 Privacy

Privacy is an important design consideration for NOVA.

Whenever possible, NOVA should support:

* Local processing
* Local models
* Local memory
* User-controlled data
* Configurable cloud services
* No unnecessary data collection

Cloud services may be used when required, but they should remain replaceable components rather than becoming the foundation of the entire system.

---

## ⚡ Philosophy

NOVA is not intended to be just another chatbot.

The long-term idea is:

```text
Chatbot
   ↓
Assistant
   ↓
Tool-Using Assistant
   ↓
Personal AI System
```

The project should remain:

**Modular • Lightweight • Private • Customizable • Useful**

---

## 🧪 Project Status

**Status:** 🚧 Active Development

NOVA is currently a personal development project and is still under construction.

Features may change significantly as the architecture evolves.

---

## 🤝 Contributions

NOVA is currently being developed primarily as a personal project.

The architecture may eventually be opened for broader contributions once the core system becomes stable.

---

## 📜 License

License information will be added when the project's distribution model is finalized.

---

## 👨‍💻 Developer

**Krishna Agrawal**

NOVA AI is being developed as a personal learning and development project combining:

* Artificial Intelligence
* Python
* Web Development
* Desktop Development
* Automation
* Local AI
* Software Architecture

---

## ⭐ NOVA

> **A personal AI system built from the ground up.**

```text
NOVA AI
Personal • Modular • Intelligent • Evolving
```
