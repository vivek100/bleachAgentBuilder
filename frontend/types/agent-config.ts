export enum AgentType {
  LLM_AGENT = "llm_agent",
  SEQUENTIAL_AGENT = "sequential_agent",
  PARALLEL_AGENT = "parallel_agent",
  LOOP_AGENT = "loop_agent",
}

export enum BuiltinToolType {
  GOOGLE_SEARCH = "google_search",
  URL_CONTEXT = "url_context",
  LOAD_MEMORY = "load_memory",
  PRELOAD_MEMORY = "preload_memory",
  LOAD_ARTIFACTS = "load_artifacts",
  TRANSFER_TO_AGENT = "transfer_to_agent",
  GET_USER_CHOICE = "get_user_choice",
  EXIT_LOOP = "exit_loop",
}

export interface ToolConfig {
  name: string
  type: "builtin" | "custom_function"
  description: string
  builtin_type?: BuiltinToolType
  function_code?: string
  imports?: string[]
  dependencies?: string[]
}

export interface AgentConfig {
  name: string
  type: AgentType
  description: string
  model?: string
  instruction?: string
  tools: string[]
  sub_agents: string[]
  config: Record<string, any>
}

export interface AgentProjectConfig {
  project_name: string
  description: string
  version: string
  main_agent: string
  agents: Record<string, AgentConfig>
  tools: Record<string, ToolConfig>
  requirements: string[]
  environment_variables: Record<string, string>
  environment_variables_example: Record<string, string>
}

export interface GraphNode {
  id: string
  type: "agent" | "tool"
  data: {
    label: string
    description: string
    agentType?: AgentType
    toolType?: "builtin" | "custom_function"
  }
  position: { x: number; y: number }
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  type: "sub_agent" | "tool_usage"
  label?: string
}
