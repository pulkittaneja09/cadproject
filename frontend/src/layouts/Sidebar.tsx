import { NavLink } from "react-router-dom";
import {
  Activity,
  LayoutDashboard,
  MessageSquare,
  Sparkles,
  Upload,
  Settings,
  ArrowUpRight,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import { useState } from "react";
const items = [
  { path: "/", label: "Overview", icon: LayoutDashboard },
  { path: "/feedback", label: "Feedback explorer", icon: MessageSquare },
  { path: "/insights", label: "Insights", icon: Sparkles },
  { path: "/import", label: "Import feedback", icon: Upload },
];
export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <NavLink to="/" className="brand" aria-label="InsightPulse home">
        <span className="brand-icon">
          <Activity size={23} />
        </span>
        <span className="brand-name">
          InsightPulse<span className="brand-ai">AI</span>
        </span>
      </NavLink>
      <div className="workspace">
        <span className="workspace-avatar">IP</span>
        <div>
          <strong>Customer intelligence</strong>
          <small>Local workspace</small>
        </div>
      </div>
      <p className="nav-label">Workspace</p>
      <nav aria-label="Main navigation">
        {items.map(({ path, label, icon: Icon }) => (
          <NavLink
            key={path}
            end={path === "/"}
            to={path}
            title={label}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <div className="sidebar-note">
          <span className="mini-orbit">
            <Sparkles size={18} />
          </span>
          <strong>Every voice, understood.</strong>
          <p>Turn customer feedback into your next move.</p>
          <NavLink to="/insights">
            Explore insights <ArrowUpRight size={14} />
          </NavLink>
        </div>
        <NavLink
          to="/settings"
          aria-label="Settings & datasets"
          className="nav-item"
        >
          <Settings size={18} />
          <span>Settings & datasets</span>
        </NavLink>
        <button
          className="collapse-button"
          aria-label={collapsed ? "Expand navigation" : "Collapse navigation"}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? (
            <PanelLeftOpen size={17} />
          ) : (
            <>
              <PanelLeftClose size={17} />
              <span>Collapse navigation</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
