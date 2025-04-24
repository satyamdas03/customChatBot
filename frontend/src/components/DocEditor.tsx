// src/components/DocEditor.tsx
import { useMemo, useState, useEffect, ChangeEvent } from "react";
import { createEditor, Descendant } from "slate";
import { Slate, Editable, withReact } from "slate-react";
import axios from "axios";
import { Input, Button, VStack, Box } from "@chakra-ui/react";

export default function DocEditor() {
  // 1. Create the editor instance
  const editor = useMemo(() => withReact(createEditor()), []);

  // 2. Define your initial document
  const initial: Descendant[] = [
    { type: "paragraph", children: [{ text: "Start typing your document..." }] } as Descendant,
  ];

  // 3. Track state for document and AI command
  const [doc, setDoc] = useState<Descendant[]>(initial);
  const [cmd, setCmd] = useState("");
  const [sessionId, setSessionId] = useState<string>("");

  // 4. Initialize or load session ID
  useEffect(() => {
    let sid = localStorage.getItem("chat_session");
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem("chat_session", sid);
    }
    setSessionId(sid);
  }, []);

  // 5. Send command to AI and update document
  const runAI = async () => {
    if (!cmd.trim()) return;
    try {
      const res = await axios.post("/chat", {
        session_id: sessionId,
        user_input: cmd,
      });
      if (res.data.document) {
        setDoc(res.data.document as Descendant[]);
      }
    } catch (error) {
      console.error("AI formatting error:", error);
    } finally {
      setCmd("");
    }
  };

  return (
    <VStack gap={4} align="stretch">
      <Box flexGrow={1} overflowY="auto">
        <Slate editor={editor} initialValue={doc} onChange={(newVal) => setDoc(newVal)}>
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
      </Box>

      <Box display="flex">
        <Input
          value={cmd}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setCmd(e.target.value)}
          placeholder="Tell the AI what to do…"
          mr={2}
        />
        <Button onClick={runAI} colorScheme="teal">
          Run AI
        </Button>
      </Box>
    </VStack>
  );
}
