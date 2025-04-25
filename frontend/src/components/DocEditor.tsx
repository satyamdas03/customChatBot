/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useMemo, useState, useEffect, ChangeEvent } from 'react';
import { createEditor, Descendant } from 'slate';
import {
  Slate,
  Editable,
  withReact,
  RenderElementProps,
  RenderLeafProps,
} from 'slate-react';
import axios from 'axios';
import { VStack, Box, Input, Button } from '@chakra-ui/react';
import { v4 as uuidv4 } from 'uuid';

export default function DocEditor() {
  //  Create the Slate editor
  const editor = useMemo(() => withReact(createEditor()), []);

  //  Session ID management
  const [sessionId, setSessionId] = useState('');
  useEffect(() => {
    let sid = localStorage.getItem('chat_session');
    if (!sid) {
      sid = uuidv4();
      localStorage.setItem('chat_session', sid);
    }
    setSessionId(sid);
  }, []);

  // Document state
  const initialValue = [
    { type: 'paragraph', children: [{ text: 'Start typing your document...' }] },
  ] as any as Descendant[];
  const [doc, setDoc] = useState<Descendant[]>(initialValue);

  // AI command state
  const [cmd, setCmd] = useState('');

  // Run AI formatting
  const runAI = async () => {
    if (!cmd.trim() || !sessionId) return;
    try {
      const res = await axios.post('/chat', {
        session_id: sessionId,
        user_input: cmd,
      });
      if (res.data.document) {
        setDoc(res.data.document as Descendant[]);
      }
    } catch (error) {
      console.error('AI formatting error', error);
    }
    setCmd('');
  };

  // RenderElement for paragraphs with alignment
  const renderElement = (props: RenderElementProps) => {
    const el = props.element as any;
    if (el.type === 'paragraph') {
      return (
        <p style={{ textAlign: el.textAlign ?? 'left', margin: '0 0 1em' }}>
          {props.children}
        </p>
      );
    }
    return <p>{props.children}</p>;
  };

  // RenderLeaf for bold and fontSize marks
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
      <Slate editor={editor} initialValue={doc} onChange={(value) => setDoc(value)}>
        <Editable
          renderElement={renderElement}
          renderLeaf={renderLeaf}
          placeholder="Type here…"
          style={{
            padding: '1rem',
            border: '1px solid #ccc',
            borderRadius: '4px',
            minHeight: '200px',
            background: 'white',
            color: 'black',
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
}
