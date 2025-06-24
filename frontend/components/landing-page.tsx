"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Send, Zap } from "lucide-react"
import { mockPrompts } from "@/lib/mock-api"
import type { PromptSuggestion } from "@/types"

interface LandingPageProps {
  onSubmit: (message: string) => void
}

export function LandingPage({ onSubmit }: LandingPageProps) {
  const [input, setInput] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      onSubmit(input.trim())
    }
  }

  const handlePromptClick = (prompt: PromptSuggestion) => {
    setInput(prompt.title)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl mx-auto animate-fade-in">
        {/* Brand Header */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white">Bleach</h1>
              <Badge
                variant="secondary"
                className="bg-blue-500/10 text-blue-400 border-blue-500/20 px-2 py-0.5 text-xs"
              >
                Beta
              </Badge>
            </div>
          </div>
        </div>

        {/* Main Heading */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">Build AI agents with ease</h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Create intelligent AI agents for your business needs. Define their personality, knowledge, and capabilities
            through simple conversation.
          </p>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="relative max-w-2xl mx-auto">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe the AI agent you want to build..."
              className="min-h-[120px] bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 resize-none pr-12 text-sm"
            />
            <Button
              type="submit"
              size="sm"
              disabled={!input.trim()}
              className="absolute bottom-3 right-3 bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </form>

        {/* Prompt Suggestions */}
        <div className="max-w-3xl mx-auto">
          <div className="flex flex-wrap justify-center gap-3">
            {mockPrompts.map((prompt, index) => (
              <button
                key={prompt.id}
                onClick={() => handlePromptClick(prompt)}
                className="group px-4 py-2 bg-slate-800/30 hover:bg-slate-800/50 border border-slate-700/50 hover:border-slate-600 rounded-full text-sm text-slate-300 hover:text-white transition-all duration-200 animate-slide-in whitespace-nowrap"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {prompt.title}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
