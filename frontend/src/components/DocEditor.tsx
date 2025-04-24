// src/components/DocEditor.tsx
import { useMemo, useState, useEffect, ChangeEvent } from "react";
import { createEditor, Descendant } from "slate";
import { Slate, Editable, withReact, RenderElementProps, RenderLeafProps } from "slate-react";
import axios from "axios";
import { Input, Button, VStack, Box } from "@chakra-ui/react";
import { v4 as uuidv4 } from "uuid";

export default function DocEditor() {
  // 1️⃣ Editor instance
  const editor = useMemo(() => withReact(createEditor()), []);

  // 2️⃣ Session ID
  const [sessionId, setSessionId] = useState<string>("");
  useEffect(() => {
    let sid = localStorage.getItem("chat_session");
    if (!sid) {
      sid = uuidv4();
      localStorage.setItem("chat_session", sid);
    }
    setSessionId(sid);
  }, []);

  // 3️⃣ Document state
  const initial = [
    { type: "paragraph", children: [{ text: "Start typing your document..." }] }
  ] as unknown as Descendant[];
  const [doc, setDoc] = useState<Descendant[]>(initial);

  // 4️⃣ User command
  const [cmd, setCmd] = useState("");

  // 5️⃣ Run AI
  const runAI = async () => {
    if (!cmd.trim() || !sessionId) return;
    try {
      const res = await axios.post("/chat", {
        session_id: sessionId,
        user_input: cmd,
      });
      if (res.data.document) {
        setDoc(res.data.document as Descendant[]);
      }
      setCmd("");
    } catch (err) {
      console.error(err);
    }
  };

  // 6️⃣ RenderElement handles paragraph alignment
  const renderElement = (props: RenderElementProps) => {
    const elem = props.element as any;  // allow custom fields
    if (elem.type === "paragraph") {
      return (
        <p style={{ textAlign: elem.textAlign || "left", margin: 0 }}>
          {props.children}
        </p>
      );
    }
    return <p>{props.children}</p>;
  };

  // 7️⃣ RenderLeaf handles marks
  const renderLeaf = (props: RenderLeafProps) => {
    let { children } = props;
    const leaf = props.leaf as any;
    const style: React.CSSProperties = {};
    if (leaf.bold) children = <strong>{children}</strong>;
    if (leaf.fontSize) style.fontSize = `${leaf.fontSize}px`;
    return <span style={style}>{children}</span>;
  };

  return (
    <VStack w="600px" p={4} gap={3} align="stretch">
      {/* Slate editor as a controlled component */}
      <Slate editor={editor} value={doc} onChange={(newVal) => setDoc(newVal)}>
        <Editable
          renderElement={renderElement}
          renderLeaf={renderLeaf}
          placeholder="Type here…"
          style={{
            padding: "1rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            minHeight: "200px",
            background: "white",
            color: "black",
          }}
        />
      </Slate>

      {/* AI command input */}
      <Box display="flex" gap={2}>
        <Input
          value={cmd}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setCmd(e.target.value)}
          placeholder="Tell the AI what to do…"
        />
        <Button onClick={runAI}>Run AI</Button>
      </Box>
    </VStack>
  );
} w="600px" p={4} gap={3} align="stretch">
      <Slate
        editor={editor}
        initialValue={doc}
        onChange={(newVal) => setDoc(newVal)}
      >
        <Editable
          renderElement={renderElement}
          renderLeaf={renderLeaf}
          placeholder="Type here…"
          style={{
            padding: "1rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            minHeight: "200px",
            background: "white",
            color: "black",
          }}
        />
      </Slate>

      <Box display="flex" gap={2}>
        <Input
          value={cmd}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setCmd(e.target.value)}
          placeholder="Tell the AI what to do…"
        />
        <Button onClick={runAI}>Run AI</Button>
      </Box>
    </VStack>
  );
}
