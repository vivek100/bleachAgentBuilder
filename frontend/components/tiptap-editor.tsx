"use client"

import { useEditor, EditorContent } from "@tiptap/react"
import StarterKit from "@tiptap/starter-kit"
import { Button } from "@/components/ui/button"
import { Bold, Italic, Code, List, ListOrdered, Quote, Maximize2, Minimize2, X } from "lucide-react"
import { useState } from "react"

interface TipTapEditorProps {
  content: string
  onChange: (content: string) => void
  placeholder?: string
  className?: string
  label?: string
}

export function TipTapEditor({ content, onChange, placeholder, className, label }: TipTapEditorProps) {
  const [isFullscreen, setIsFullscreen] = useState(false)

  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        codeBlock: {
          HTMLAttributes: {
            class: "bg-slate-900 text-green-400 p-4 rounded-md font-mono text-sm",
          },
        },
      }),
    ],
    content,
    onUpdate: ({ editor }) => {
      onChange(editor.getHTML())
    },
    editorProps: {
      attributes: {
        class: `prose prose-sm max-w-none focus:outline-none p-3 text-slate-700 ${
          isFullscreen ? "min-h-[calc(100vh-200px)]" : "min-h-[120px]"
        }`,
      },
    },
  })

  if (!editor) {
    return (
      <div className={`border border-slate-200 rounded-md ${className}`}>
        <div className="p-3 min-h-[120px] text-slate-500 text-sm">Loading editor...</div>
      </div>
    )
  }

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  const ToolbarContent = () => (
    <div className="border-b border-slate-200 p-2 flex items-center justify-between">
      <div className="flex items-center gap-1">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleBold().run()}
          className={`h-8 px-2 ${editor.isActive("bold") ? "bg-slate-200" : ""}`}
        >
          <Bold className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleItalic().run()}
          className={`h-8 px-2 ${editor.isActive("italic") ? "bg-slate-200" : ""}`}
        >
          <Italic className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleCode().run()}
          className={`h-8 px-2 ${editor.isActive("code") ? "bg-slate-200" : ""}`}
        >
          <Code className="w-4 h-4" />
        </Button>
        <div className="w-px h-6 bg-slate-200 mx-1" />
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          className={`h-8 px-2 ${editor.isActive("bulletList") ? "bg-slate-200" : ""}`}
        >
          <List className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
          className={`h-8 px-2 ${editor.isActive("orderedList") ? "bg-slate-200" : ""}`}
        >
          <ListOrdered className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => editor.chain().focus().toggleBlockquote().run()}
          className={`h-8 px-2 ${editor.isActive("blockquote") ? "bg-slate-200" : ""}`}
        >
          <Quote className="w-4 h-4" />
        </Button>
        <div className="w-px h-6 bg-slate-200 mx-1" />
        <Button variant="ghost" size="sm" onClick={toggleFullscreen} className="h-8 px-2">
          {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
        </Button>
      </div>
    </div>
  )

  if (isFullscreen) {
    return (
      <div className="fixed inset-0 z-50 bg-white flex flex-col">
        {/* Fullscreen Header */}
        <div className="border-b border-slate-200 p-4 flex items-center justify-between bg-slate-50">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              {label ? `Editing: ${label}` : "Full Screen Editor"}
            </h2>
            <p className="text-sm text-slate-600">Press Escape or click minimize to exit fullscreen</p>
          </div>
          <Button variant="ghost" size="sm" onClick={toggleFullscreen} className="h-8 px-2">
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Fullscreen Toolbar */}
        <ToolbarContent />

        {/* Fullscreen Editor */}
        <div className="flex-1 overflow-y-auto">
          <EditorContent editor={editor} className="h-full" />
        </div>

        {/* Fullscreen Footer */}
        <div className="border-t border-slate-200 p-4 bg-slate-50">
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={toggleFullscreen}>
              Done Editing
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`border border-slate-200 rounded-md ${className}`}>
      <ToolbarContent />
      <EditorContent editor={editor} className="min-h-[120px]" />
    </div>
  )
}
