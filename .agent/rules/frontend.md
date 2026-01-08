---
trigger: always_on
---

### **Frontend Architecture Rules**

#### **1. Types & Interfaces**

* **Location:** `frontend/lib/types` (or designated directory).
* **Rule:** Define explicit TypeScript `interface` or `type` for every Request payload and Response body.
* **Naming:** Use the format `[Feature][Action]Request` and `[Feature][Action]Response` (e.g., `UserLoginRequest`).
* **Exporting:** Maintain an **`index.ts`** file to export all types from a single entry point.

#### **2. API Services**

* **Location:** `frontend/lib/services` (or designated directory).
* **Rule:** Create a class or set of functions for each API domain. Use a pre-configured Axios instance or Fetch wrapper.
* **Responsibility:** Services should only handle data fetching, headers, and error mapping. They should not contain UI logic.
* **Exporting:** Maintain an **`index.ts`** file to export all service functions/classes for easy access.

#### **3. Custom Hooks**

* **Location:** `frontend/lib/hooks/api`
* **Rule:** Use standard **React Hooks (`useState`, `useEffect`)** to manage API states (data, loading, error). **Do not use TanStack Query.**
* **Naming:** Use **kebab-case** format: `use-[action]-[feature]` (e.g., `use-get-profile`, `use-post-login`).
* **Exporting:** Maintain an **`index.ts`** file to export all hooks, allowing for barrel imports like `import { use-get-profile } from '@/lib/hooks/api'`.