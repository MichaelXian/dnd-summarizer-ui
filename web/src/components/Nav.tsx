import React from 'react';
import { NavLink } from 'react-router-dom';

const linkStyle: React.CSSProperties = {
  padding: '0.5rem 0.75rem',
  borderRadius: 6,
  textDecoration: 'none',
};

const Nav: React.FC = () => {
  return (
    <nav style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center', marginBottom: '1rem' }}>
      <NavLink to="/" style={({ isActive }) => ({ ...linkStyle, background: isActive ? '#eef7ff' : 'transparent' })} end>
        Upload
      </NavLink>
      <NavLink to="/summary" style={({ isActive }) => ({ ...linkStyle, background: isActive ? '#eef7ff' : 'transparent' })}>
        Summary
      </NavLink>
      <NavLink to="/chat" style={({ isActive }) => ({ ...linkStyle, background: isActive ? '#eef7ff' : 'transparent' })}>
        Chat
      </NavLink>
    </nav>
  );
};

export default Nav;
