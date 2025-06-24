export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

export interface AppState {
  isBuilding: boolean
  isComplete: boolean
  progress: number
}

export interface PromptSuggestion {
  id: string
  title: string
  description: string
}
