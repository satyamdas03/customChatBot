import { Box, VStack, Input, Button, Text, Spinner } from "@chakra-ui/react";
import { useState, useEffect } from "react";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

type Message = { role: string; content: string };

export default function ChatWindow() {
  const [msgs, setMsgs] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [sessionId, setSessionId] = useState<string>();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let sid = localStorage.getItem("chat_session");
    if (!sid) {
      sid = uuidv4();
      localStorage.setItem("chat_session", sid);
    }
    setSessionId(sid);
  }, []);

  const send = async () => {
    if (!text.trim() || !sessionId) return;
    setMsgs((m) => [...m, { role: "user", content: text }]);
    setLoading(true);

    try {
      const res = await axios.post("/chat", {
        session_id: sessionId,
        user_input: text,
      });
      setMsgs((m) => [
        ...m,
        { role: "assistant", content: res.data.response },
      ]);
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : String(err);
      setMsgs((m) => [
        ...m,
        { role: "assistant", content: `⚠️ Error: ${msg}` },
      ]);
    } finally {
      setLoading(false);
      setText("");
    }
  };

  return (
    <VStack
      w="400px"
      h="600px"
      border="1px solid"
      borderColor="gray.600"
      borderRadius="lg"
      p={4}
      gap={3}
      align="stretch"
      bg="gray.700"
    >
      <Box flexGrow={1} overflowY="auto" px={2}>
        {msgs.map((m, i) => (
          <Box
            key={i}
            bg={m.role === "user" ? "blue.200" : "gray.200"}
            color="black"                     // force black text
            alignSelf={m.role === "user" ? "flex-end" : "flex-start"}
            px={4}
            py={2}
            borderRadius="md"
            mb={2}
            maxW="80%"
            boxShadow="sm"
          >
            <Text>{m.content}</Text>
          </Box>
        ))}
        {loading && (
          <Spinner size="sm" alignSelf="flex-start" mt={2} color="teal.300" />
        )}
      </Box>

      <Box display="flex">
        <Input
          value={text}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setText(e.target.value)
          }
          placeholder="Type a message…"
          mr={2}
          onKeyDown={(e) => {
            if (e.key === "Enter") send();
          }}
          bg="gray.600"
          color="white"
          _placeholder={{ color: "gray.400" }}
        />
        <Button loading={loading} onClick={send} colorScheme="teal">
          Send
        </Button>
      </Box>
    </VStack>
  );
}
