import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Budgets from "./pages/Budgets";
import Goals from "./pages/Goals";
import Chat from "./pages/Chat";
import Reports from "./pages/Reports";
import Admin from "./pages/Admin";
import AppLayout from "./components/AppLayout";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<Dashboard />} />
      </Route>
      <Route path="/home" element={<Home />} />
      <Route path="/app" element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="transactions" element={<Transactions />} />
        <Route path="budgets" element={<Budgets />} />
        <Route path="goals" element={<Goals />} />
        <Route path="chat" element={<Chat />} />
        <Route path="reports" element={<Reports />} />
        <Route path="admin" element={<Admin />} />
      </Route>
      <Route path="/dashboard" element={<AppLayout />}>
        <Route index element={<Dashboard />} />
      </Route>
      <Route path="/analytics" element={<AppLayout />}>
        <Route index element={<Dashboard />} />
      </Route>
      <Route path="/ai-assistant" element={<AppLayout />}>
        <Route index element={<Chat />} />
      </Route>
      <Route path="/budget-planner" element={<AppLayout />}>
        <Route index element={<Budgets />} />
      </Route>
      <Route path="/reports" element={<AppLayout />}>
        <Route index element={<Reports />} />
      </Route>
    </Routes>
  );
}
