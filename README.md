# AI-Driven Factory Layout Generation Using Natural Language Prompts  
### Metaverse AI Internship – Makers Lab, Tech Mahindra  
Dhanush V, NIT Karnataka

---

## Overview
This project focuses on enhancing NVIDIA Omniverse’s ChatUSD platform to enable accurate, AI-driven factory layout generation using natural language prompts. The baseline ChatUSD system faced several limitations, including objects spawning at the origin (0,0,0), failure to detect ground meshes, lack of collision awareness, and incorrect interpretation of spatial instructions such as “place the forklift behind the container on the ground.” These issues motivated a multi-phase R&D approach to bridge the gap between human intent and precise 3D scene construction.
:contentReference[oaicite:0]{index=0}

---

## Key Contributions

### Phase 1: Custom Agent Integration
- Implemented a Greeting Agent to validate agent extensibility within ChatUSD’s multi-agent architecture.  
- Established effective inter-agent communication and verified retrieval of scene information such as prims and properties.  
:contentReference[oaicite:1]{index=1}

### Phase 2: Prompt Simplifier (Decomposer Agent)
- Built a Prompt Simplifier Agent to break complex user instructions into clear, atomic, sequential steps.  
- Significantly improved reliability by reducing hallucinations and enhancing USD code accuracy.  
- Enabled step-wise user control and predictable 3D scene generation.  
:contentReference[oaicite:2]{index=2}

### Phase 3.1: Spatial Reasoning Using Custom Agents
- Developed a Spatial Agent to understand spatial relationships such as on, under, beside, and behind.  
- Introduced ground alignment rules, fallback behaviors, and improved placement accuracy.  
- Resulted in more realistic, structured, and collision-free industrial layouts.  
:contentReference[oaicite:3]{index=3}

### Phase 3.2: Spatial Intelligence using Gemini
- Integrated Gemini 2.5 Flash for advanced spatial reasoning.  
- Explored four architectural approaches: function-call method, orchestrator-based routing, dedicated Gemini Spatial Agent, and wrapper-based enhancement.  
- Enabled deeper spatial interpretation and improved multi-model coordination without disrupting core ChatUSD design principles.  
:contentReference[oaicite:4]{index=4}

---

## Overall Impact
- Enhanced ChatUSD from a basic scene generator to a spatially intelligent layout construction system.  
- Achieved consistent and accurate placement of objects across industrial scenes.  
- Provided structure, transparency, and reliability in prompt-driven 3D design workflows.  
:contentReference[oaicite:5]{index=5}

---

## Tools and Technologies
- NVIDIA Omniverse Kit 107.3  
- ChatUSD 2.0.4  
- Python, USD APIs  
- LangChain Agent Framework  
- Google Gemini 2.5 Flash  
:contentReference[oaicite:6]{index=6}

---

## Internship Duration
19 May 2025 – 18 July 2025  
:contentReference[oaicite:7]{index=7}

---

## Future Scope
- Broader domain semantics for industrial components  
- Automated optimisation strategies for collision-free layouts  
- Advanced multi-agent orchestration across LLMs  
:contentReference[oaicite:8]{index=8}

---

## Report
The complete internship report is available in this repository.
