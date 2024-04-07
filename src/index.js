import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { useState } from 'react';

import App from "./App";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <App />
  </StrictMode>
);

function useDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return { isOpen, toggleDropdown };
}

export default useDropdown;
