# Technical Design: Agentic Service Discovery & Registration

**Project Name:** Expedia-Agentic-DevPortal (Prototype)  
**Author:** Dinesh Kumar, Microsoft MVP (AI) & Senior Product Manager  
**Tech Stack:** Model Context Protocol (MCP), Python (FastMCP), Backstage (Spotify), LLM (Claude 3.5 Sonnet)

---

## 1. Executive Summary

Modern developer portals like Backstage are essential for managing microservices at scale but often suffer from high discovery friction. This prototype demonstrates an **Agentic Developer Experience (DevEx)** layer that allows engineers to audit, discover, and register software components using natural language via the Model Context Protocol (MCP).

---

## 2. The Problem Statement

In a complex ecosystem like Expedia's, developers face:

- **Discovery Fatigue:** Navigating thousands of services in the Catalog to find ownership or API details.
- **Onboarding Friction:** Manually creating `catalog-info.yaml` files and following "Golden Path" standards.
- **Disconnected Tooling:** Switching between the portal UI, CLI, and documentation.

---

## 3. Proposed Architecture

The solution bridges the gap between the engineer's intent and the platform's infrastructure using three layers:

| Layer | Role |
|---|---|
| **The Interface (LLM)** | Acts as the primary interaction point, translating natural language into structured API calls. |
| **The Bridge (MCP Server)** | A local Python server that exposes "Tools" to the LLM. It acts as the secure execution environment for internal commands. |
| **The Target (Backstage API)** | The source of truth where services are registered and queried. |

---

## 4. Core Features (The "Breakthrough" Work)

| Capability | Implementation Detail | Value |
|---|---|---|
| **Real-time Audit** | Queries the `/api/catalog/entities` endpoint to fetch live component data. | Instant visibility without manual searching. |
| **Agentic Registration** | Generates schema-compliant YAML files and persists them to the Backstage source. | Automates the "Golden Path" for new service creation. |
| **Contextual Discovery** | LLM-driven filtering (e.g., *"Find all services owned by the guests team"*). | Reduces cognitive load for new engineers. |

---

## 5. Scalability & Security Considerations

- **Standardization:** By using MCP, we avoid building custom one-off integrations. This protocol can be extended to support CI/CD status, Kubernetes logs, or Sentry errors.
- **Governance:** The AI Agent acts as a validator, ensuring every `register_new_service` call includes mandatory metadata (Owner, Lifecycle, System) before execution.