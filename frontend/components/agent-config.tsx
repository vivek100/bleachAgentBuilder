"use client"

import { useState, useEffect } from "react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Download, Settings, Network, Save, X, Key, Info } from "lucide-react"
import { AgentGraph } from "./agent-graph"
import { CodeEditor } from "./code-editor"
import { TipTapEditor } from "./tiptap-editor"
import type { AgentProjectConfig, AgentConfig, ToolConfig } from "@/types/agent-config"
import { fetchAgentConfig, updateAgent, updateTool } from "@/lib/agent-api"
import { codeGenerator } from "@/lib/code-generator"

interface EditingState {
  type: "agent" | "tool" | null
  id: string | null
  data: AgentConfig | ToolConfig | null
}

export function AgentConfig() {
  const [config, setConfig] = useState<AgentProjectConfig | null>(null)
  const [loading, setLoading] = useState(true)
  const [editingState, setEditingState] = useState<EditingState>({
    type: null,
    id: null,
    data: null,
  })
  const [saving, setSaving] = useState(false)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const data = await fetchAgentConfig()
        setConfig(data)
      } catch (error) {
        console.error("Failed to load config:", error)
      } finally {
        setLoading(false)
      }
    }

    loadConfig()
  }, [])

  const handleNodeClick = (nodeId: string, nodeType: "agent" | "tool") => {
    if (!config) return

    // Clear previous editing state first
    setEditingState({ type: null, id: null, data: null })

    // Set new editing state
    setTimeout(() => {
      if (nodeType === "agent" && config.agents[nodeId]) {
        setEditingState({
          type: "agent",
          id: nodeId,
          data: { ...config.agents[nodeId] },
        })
      } else if (nodeType === "tool" && config.tools[nodeId]) {
        setEditingState({
          type: "tool",
          id: nodeId,
          data: { ...config.tools[nodeId] },
        })
      }
    }, 50)
  }

  const handleSave = async () => {
    if (!editingState.data || !editingState.id || !config) return

    setSaving(true)
    try {
      if (editingState.type === "agent") {
        const agentData = editingState.data as AgentConfig
        await updateAgent(editingState.id, agentData)
        setConfig({
          ...config,
          agents: {
            ...config.agents,
            [editingState.id]: agentData,
          },
        })
      } else if (editingState.type === "tool") {
        const toolData = editingState.data as ToolConfig
        await updateTool(editingState.id, toolData)
        setConfig({
          ...config,
          tools: {
            ...config.tools,
            [editingState.id]: toolData,
          },
        })
      }

      // Clear editing state after successful save
      setEditingState({ type: null, id: null, data: null })
    } catch (error) {
      console.error("Failed to save:", error)
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    setEditingState({ type: null, id: null, data: null })
  }

  const updateEditingData = (updates: Partial<AgentConfig | ToolConfig>) => {
    if (!editingState.data) return

    setEditingState({
      ...editingState,
      data: { ...editingState.data, ...updates },
    })
  }

  const handleDownloadCode = async () => {
    if (!config) return

    setDownloading(true)
    try {
      await codeGenerator.generateAndDownload(config)
    } catch (error) {
      console.error("Failed to generate code:", error)
    } finally {
      setDownloading(false)
    }
  }

  if (loading) {
    return (
      <div className="h-full bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-sm text-slate-600">Loading agent configuration...</p>
        </div>
      </div>
    )
  }

  if (!config) {
    return (
      <div className="h-full bg-slate-50 flex items-center justify-center">
        <p className="text-sm text-slate-600">Failed to load configuration</p>
      </div>
    )
  }

  const editingAgent = editingState.type === "agent" ? (editingState.data as AgentConfig) : null
  const editingTool = editingState.type === "tool" ? (editingState.data as ToolConfig) : null

  return (
    <div className="h-full bg-slate-50 flex flex-col">
      <div className="flex-1 overflow-hidden">
        <Tabs defaultValue="graph" className="h-full flex flex-col">
          <div className="p-4 border-b border-slate-200 bg-white flex-shrink-0">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900">{config.project_name}</h2>
                <p className="text-slate-600 text-sm">{config.description}</p>
              </div>
              <div className="flex gap-2">
                <Button size="sm" onClick={handleDownloadCode} disabled={downloading}>
                  <Download className="w-4 h-4 mr-2" />
                  {downloading ? "Generating..." : "Download Code"}
                </Button>
              </div>
            </div>

            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="graph" className="flex items-center gap-2">
                <Network className="w-4 h-4" />
                Graph View
              </TabsTrigger>
              <TabsTrigger value="settings" className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Project Settings
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-hidden">
            <TabsContent value="graph" className="h-full m-0 p-0">
              <div className="h-full flex">
                <div className="flex-1">
                  <AgentGraph config={config} onNodeClick={handleNodeClick} />
                </div>

                {/* Side panel for editing */}
                {editingState.data && (
                  <div className="w-96 border-l border-slate-200 bg-white flex flex-col">
                    <div className="p-4 border-b border-slate-200 flex items-center justify-between">
                      <h3 className="font-semibold text-slate-900">
                        {editingAgent ? `Edit Agent: ${editingAgent.name}` : `Edit Tool: ${editingTool?.name}`}
                      </h3>
                      <Button variant="ghost" size="sm" onClick={handleCancel}>
                        <X className="w-4 h-4" />
                      </Button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                      {editingAgent && (
                        <>
                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Name</label>
                            <Input
                              value={editingAgent.name}
                              onChange={(e) => updateEditingData({ name: e.target.value })}
                              className="text-sm"
                            />
                          </div>

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Description</label>
                            <Textarea
                              value={editingAgent.description}
                              onChange={(e) => updateEditingData({ description: e.target.value })}
                              className="text-sm"
                              rows={2}
                            />
                          </div>

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Type</label>
                            <Badge variant="outline" className="text-xs">
                              {editingAgent.type}
                            </Badge>
                          </div>

                          {editingAgent.model && (
                            <div>
                              <label className="text-sm font-medium text-slate-700 mb-1 block">Model</label>
                              <Input
                                value={editingAgent.model}
                                onChange={(e) => updateEditingData({ model: e.target.value })}
                                className="text-sm"
                              />
                            </div>
                          )}

                          {editingAgent.instruction && (
                            <div>
                              <label className="text-sm font-medium text-slate-700 mb-1 block">Instructions</label>
                              <TipTapEditor
                                content={editingAgent.instruction}
                                onChange={(content) => updateEditingData({ instruction: content })}
                                placeholder="Enter agent instructions..."
                                label={`${editingAgent.name} Instructions`}
                              />
                            </div>
                          )}

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Tools</label>
                            <div className="flex flex-wrap gap-1">
                              {editingAgent.tools.map((tool) => (
                                <Badge key={tool} variant="secondary" className="text-xs">
                                  {tool}
                                </Badge>
                              ))}
                            </div>
                          </div>

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Sub Agents</label>
                            <div className="flex flex-wrap gap-1">
                              {editingAgent.sub_agents.map((subAgent) => (
                                <Badge key={subAgent} variant="outline" className="text-xs">
                                  {subAgent}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </>
                      )}

                      {editingTool && (
                        <>
                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Name</label>
                            <Input
                              value={editingTool.name}
                              onChange={(e) => updateEditingData({ name: e.target.value })}
                              className="text-sm"
                            />
                          </div>

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Description</label>
                            <Textarea
                              value={editingTool.description}
                              onChange={(e) => updateEditingData({ description: e.target.value })}
                              className="text-sm"
                              rows={2}
                            />
                          </div>

                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Type</label>
                            <Badge variant="outline" className="text-xs">
                              {editingTool.type}
                            </Badge>
                          </div>

                          {editingTool.imports && editingTool.imports.length > 0 && (
                            <div>
                              <label className="text-sm font-medium text-slate-700 mb-1 block">Imports</label>
                              <div className="space-y-1">
                                {editingTool.imports.map((imp, index) => (
                                  <code key={index} className="block text-xs bg-slate-100 p-1 rounded">
                                    {imp}
                                  </code>
                                ))}
                              </div>
                            </div>
                          )}

                          {editingTool.dependencies && editingTool.dependencies.length > 0 && (
                            <div>
                              <label className="text-sm font-medium text-slate-700 mb-1 block">Dependencies</label>
                              <div className="flex flex-wrap gap-1">
                                {editingTool.dependencies.map((dep) => (
                                  <Badge key={dep} variant="secondary" className="text-xs">
                                    {dep}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}

                          {editingTool.function_code && (
                            <div>
                              <label className="text-sm font-medium text-slate-700 mb-1 block">Function Code</label>
                              <CodeEditor
                                value={editingTool.function_code}
                                onChange={(value) => updateEditingData({ function_code: value })}
                                language="python"
                                placeholder="Enter Python function code..."
                                label={`${editingTool.name} Function`}
                              />
                            </div>
                          )}
                        </>
                      )}
                    </div>

                    <div className="p-4 border-t border-slate-200">
                      <div className="flex gap-2">
                        <Button onClick={handleSave} className="flex-1" disabled={saving}>
                          <Save className="w-4 h-4 mr-2" />
                          {saving ? "Saving..." : "Save Changes"}
                        </Button>
                        <Button variant="outline" onClick={handleCancel}>
                          Cancel
                        </Button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="settings" className="h-full m-0 p-4 overflow-y-auto">
              <div className="max-w-4xl mx-auto space-y-6">
                {/* Project Info */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Info className="w-5 h-5 text-blue-600" />
                      Project Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium text-slate-700 mb-1 block">Project Name</label>
                        <Input value={config.project_name} className="text-sm" readOnly />
                      </div>
                      <div>
                        <label className="text-sm font-medium text-slate-700 mb-1 block">Version</label>
                        <Input value={config.version} className="text-sm" readOnly />
                      </div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-slate-700 mb-1 block">Description</label>
                      <Textarea value={config.description} className="text-sm" rows={2} readOnly />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-slate-700 mb-1 block">Main Agent</label>
                      <Input value={config.main_agent} className="text-sm" readOnly />
                    </div>
                  </CardContent>
                </Card>

                {/* Environment Variables */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Key className="w-5 h-5 text-green-600" />
                      Environment Variables
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {Object.entries(config.environment_variables).map(([key, value]) => (
                        <div key={key} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">{key}</label>
                            <Input
                              value={value}
                              className="text-sm font-mono"
                              type={
                                key.toLowerCase().includes("key") || key.toLowerCase().includes("secret")
                                  ? "password"
                                  : "text"
                              }
                              readOnly
                            />
                          </div>
                          <div>
                            <label className="text-sm font-medium text-slate-500 mb-1 block">Example Value</label>
                            <Input
                              value={config.environment_variables_example[key] || ""}
                              className="text-sm font-mono text-slate-500"
                              readOnly
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Requirements */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Settings className="w-5 h-5 text-purple-600" />
                      Python Requirements
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {config.requirements.map((req) => (
                        <Badge key={req} variant="outline" className="text-sm font-mono">
                          {req}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Statistics */}
                <Card>
                  <CardHeader>
                    <CardTitle>Project Statistics</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">{Object.keys(config.agents).length}</div>
                        <div className="text-sm text-slate-600">Total Agents</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600">{Object.keys(config.tools).length}</div>
                        <div className="text-sm text-slate-600">Total Tools</div>
                      </div>
                      <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">{config.requirements.length}</div>
                        <div className="text-sm text-slate-600">Dependencies</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </div>
  )
}
