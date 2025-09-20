interface ImportMetaEnv {
  readonly VITE_BACKEND_URL?: string;
  readonly VITE_CALENDAR_URL?: string;
  readonly VITE_CORE_URL?: string;
  readonly VITE_MCP_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}