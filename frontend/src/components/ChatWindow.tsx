// src/components/ChatWindow.tsx
import React, { ChangeEvent, useState } from "react";
import { Box, VStack, Input, Button, Text } from "@chakra-ui/react";

export default function ChatWindow() {
  const [msgs, setMsgs] = useState<{ role: string; content: string }[]>([]);
  const [text, setText] = useState("");

  // For now, just echo locally
  const send = () => {
    if (!text.trim()) return;
    setMsgs([...msgs, { role: "user", content: text }, { role: "assistant", content: text }]);
    setText("");
  };

  return (
    <VStack
      w="400px"
      h="600px"
      border="1px solid"
      borderColor="gray.200"
      borderRadius="lg"
      p={4}
      gap={3}
      align="stretch"
    >
      <Box flexGrow={1} overflowY="auto">
        {msgs.map((m, i) => (
          <Box
            key={i}
            bg={m.role === "user" ? "blue.50" : "gray.50"}
            alignSelf={m.role === "user" ? "flex-end" : "flex-start"}
            px={3}
            py={2}
            borderRadius="md"
            mb={2}
          >
            <Text>{m.content}</Text>
          </Box>
        ))}
      </Box>

      <Box display="flex">
        <Input
          value={text}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setText(e.target.value)}
          placeholder="Type a message…"
          mr={2}
        />
        <Button onClick={send}>Send</Button>
      </Box>
    </VStack>
  );
}
