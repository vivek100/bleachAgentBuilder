"use client"

import { useState } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Copy, Check, Maximize2, Minimize2, X } from "lucide-react"

interface CodeEditorProps {
  value: string
  onChange: (value: string) => void
  language?: string
  placeholder?: string
  className?: string
  label?: string
}

export function CodeEditor({ value, onChange, language = "python", placeholder, className, label }: CodeEditorProps) {
  const [copied, setCopied] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(value)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  const HeaderContent = () => (
    <div className="flex items-center justify-between mb-2">
      <div className="flex items-center gap-2">
        <span className="text-xs font-medium text-slate-600 uppercase tracking-wide">{language}</span>
        {label && <span className="text-sm font-medium text-slate-700">{label}</span>}
      </div>
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="sm" onClick={handleCopy} className="h-6 px-2 text-xs">
          {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
        </Button>
        <Button variant="ghost" size="sm" onClick={toggleFullscreen} className="h-6 px-2">
          {isFullscreen ? <Minimize2 className="w-3 h-3" /> : <Maximize2 className="w-3 h-3" />}
        </Button>
      </div>
    </div>
  )

  if (isFullscreen) {
    return (
      <div className="fixed inset-0 z-50 bg-slate-900 flex flex-col">
        {/* Fullscreen Header */}
        <div className="border-b border-slate-700 p-4 flex items-center justify-between bg-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-white">
              {label ? `Editing: ${label}` : `${language.toUpperCase()} Code Editor`}
            </h2>
            <p className="text-sm text-slate-400">Press Escape or click minimize to exit fullscreen</p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleFullscreen}
            className="h-8 px-2 text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Fullscreen Toolbar */}
        <div className="border-b border-slate-700 p-4 bg-slate-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">{language}</span>
              <div className="w-px h-4 bg-slate-600" />
              <span className="text-xs text-slate-400">{value.split("\n").length} lines</span>
              <span className="text-xs text-slate-400">{value.length} characters</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              className="h-6 px-2 text-xs text-slate-400 hover:text-white"
            >
              {copied ? <Check className="w-3 h-3 mr-1" /> : <Copy className="w-3 h-3 mr-1" />}
              {copied ? "Copied!" : "Copy"}
            </Button>
          </div>
        </div>

        {/* Fullscreen Editor */}
        <div className="flex-1 p-4">
          <Textarea
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            className="w-full h-full font-mono text-sm bg-slate-900 text-green-400 border-slate-700 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            spellCheck={false}
          />
        </div>

        {/* Fullscreen Footer */}
        <div className="border-t border-slate-700 p-4 bg-slate-800">
          <div className="flex justify-end gap-2">
            <Button
              variant="outline"
              onClick={toggleFullscreen}
              className="bg-slate-700 border-slate-600 text-white hover:bg-slate-600"
            >
              Done Editing
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      <HeaderContent />
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="font-mono text-sm min-h-[200px] bg-slate-900 text-green-400 border-slate-700 resize-none"
        spellCheck={false}
      />
    </div>
  )
}
