import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import "./index.css";

import QueryProvider from "./providers/QueryProvider";
import AuthProvider from "./context/AuthProvider";
ReactDOM.createRoot(
  document.getElementById(
    "root"
  )!
).render(
  <React.StrictMode>
    <QueryProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </QueryProvider>
  </React.StrictMode>,
);
