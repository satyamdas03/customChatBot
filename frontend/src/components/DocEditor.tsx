// src/components/DocEditor.tsx
import { useMemo, useState } from "react"
import { createEditor, Descendant } from "slate"
import { Slate, Editable, withReact } from "slate-react"

export default function DocEditor() {
  // 1. Create the editor instance
  const editor = useMemo(() => withReact(createEditor()), [])

  // 2. Define your initial document – cast to Descendant[] so `type` is allowed
  const initial: Descendant[] = [
    {
      type: "paragraph",
      children: [{ text: "Start typing your document..." }],
    } as Descendant, 
  ]

  // 3. Track state
  const [value, setValue] = useState<Descendant[]>(initial)

  return (
    <Slate
      editor={editor}
      initialValue={value}         // use `initialValue` instead of `value`
      onChange={(newVal) => setValue(newVal)}
    >
      <Editable
        placeholder="Type here…"
        style={{
          padding: "1rem",
          border: "1px solid #ccc",
          borderRadius: "4px",
          minHeight: "200px",
        }}
      />
    </Slate>
  )
}
