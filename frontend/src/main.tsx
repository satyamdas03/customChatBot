// src/main.tsx
import ReactDOM from "react-dom/client";
import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import App from "./App";
import "./index.css";  // if you have global CSS


ReactDOM.createRoot(document.getElementById("root")!).render(
  <ChakraProvider value={defaultSystem}>
    <App />
  </ChakraProvider>
);
