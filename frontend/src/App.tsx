import { Flex } from "@chakra-ui/react";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  return (
    <Flex
      w="100vw"          // full viewport width
      h="100vh"          // full viewport height
      justify="center"   // horizontal centering
      align="center"     // vertical centering
      bg="gray.800"      // optional: background so you see the contrast
    >
      <ChatWindow />
    </Flex>
  );
}
