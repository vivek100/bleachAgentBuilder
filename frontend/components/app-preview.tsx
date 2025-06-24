"use client"

import { useState, useEffect } from "react"
import { Progress } from "@/components/ui/progress"
import { MessageSquare, Settings, Bot, Download, Github } from "lucide-react"
import type { AppState } from "@/types"
import { simulateAgentBuilding } from "@/lib/mock-api"
import { AgentChat } from "./agent-chat"
import { AgentConfig } from "./agent-config"
import { Button } from "@/components/ui/button"
import { codeGenerator } from "@/lib/code-generator"
import { fetchAgentConfig } from "@/lib/agent-api"

interface AppPreviewProps {
  isVisible: boolean
}

export function AppPreview({ isVisible }: AppPreviewProps) {
  const [appState, setAppState] = useState<AppState>({
    isBuilding: true,
    isComplete: false,
    progress: 0,
  })
  const [activeTab, setActiveTab] = useState<"chat" | "config">("chat")
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    if (isVisible && appState.isBuilding) {
      simulateAgentBuilding((progress) => {
        setAppState((prev) => ({ ...prev, progress }))
        if (progress === 100) {
          setTimeout(() => {
            setAppState((prev) => ({
              ...prev,
              isBuilding: false,
              isComplete: true,
            }))
          }, 500)
        }
      })
    }
  }, [isVisible, appState.isBuilding])

  const handleDownloadCode = async () => {
    setDownloading(true)
    try {
      const config = await fetchAgentConfig()
      await codeGenerator.generateAndDownload(config)
    } catch (error) {
      console.error("Failed togenerate code:", error)
    } finally {
      setDownloading(false)
    }
  }

  if (!isVisible) {
    return (
      <div className="h-full bg-slate-900 flex items-center justify-center">
        <div className="text-center text-slate-500">
          <div className="w-16 h-16 mx-auto mb-4 rounded-lg bg-slate-800 flex items-center justify-center">
            <Bot className="w-8 h-8" />
          </div>
          <p className="text-sm">Your AI agent will appear here</p>
        </div>
      </div>
    )
  }

  if (appState.isBuilding) {
    return (
      <div className="h-full bg-slate-900 flex items-center justify-center p-8">
        <div className="w-full max-w-md text-center">
          <div className="mb-8">
            <div className="w-20 h-20 mx-auto mb-4 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center animate-pulse-slow">
              <div className="w-10 h-10 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Building your AI agent...</h3>
            <p className="text-sm text-slate-400">Training the model and setting up capabilities</p>
          </div>

          <div className="space-y-3">
            <Progress value={appState.progress} className="h-2" />
            <p className="text-xs text-slate-500">{appState.progress}% complete</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full bg-slate-900 flex flex-col">
      {/* Header with Tabs */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-4">
          <h3 className="text-sm font-medium text-white">AI Agent Preview</h3>
          <div className="flex bg-slate-800 rounded-lg p-1">
            <button
              onClick={() => setActiveTab("chat")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === "chat" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              <MessageSquare className="w-3 h-3 mr-1.5 inline" />
              Chat
            </button>
            <button
              onClick={() => setActiveTab("config")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === "config" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              <Settings className="w-3 h-3 mr-1.5 inline" />
              Config
            </button>
          </div>
        </div>

        {/* Download and GitHub buttons - moved to right corner */}
        {appState.isComplete && (
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={handleDownloadCode}
              disabled={downloading}
              className="bg-slate-800/50 border-slate-600 text-slate-200 hover:bg-slate-700 hover:border-slate-500 hover:text-white transition-all duration-200 text-xs px-3 py-1.5 h-8 font-medium"
            >
              <Download className="w-3.5 h-3.5 mr-1.5" />
              {downloading ? "Generating..." : "Download Agent Code"}
            </Button>
            <Button
              size="sm"
              variant="outline"
              className="bg-slate-800/50 border-slate-600 text-slate-200 hover:bg-slate-700 hover:border-slate-500 hover:text-white transition-all duration-200 text-xs px-3 py-1.5 h-8 font-medium"
            >
              <Github className="w-3.5 h-3.5 mr-1.5" />
              GitHub
            </Button>
          </div>
        )}
      </div>

      {/* Tab Content - constrained height */}
      <div className="flex-1 min-h-0 animate-fade-in">{activeTab === "chat" ? <AgentChat /> : <AgentConfig />}</div>
    </div>
  )
}
