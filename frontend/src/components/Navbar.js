import React from 'react';
import '../App.css'

function Navbar({ onClick, aboutRef, searchRef, user, onLogout }) {
  return (
    <div className="navigation">
      <nav className="text-white navbar navbar-dark bg-dark d-flex sawarabi-mincho-regular">
        <div className="flex-grow-1 p-2">PinyImage</div>
        <div className="text-danger p-2 pr-5 cursor" onClick={() => onClick(searchRef)}>Card Search</div>
        <div className="p-2 pr-5 cursor" onClick={() => onClick(aboutRef)}>What is PinyImage?</div>
        {user && (
          <div className="d-flex align-items-center">
            <span className="p-2 text-light">Welcome, {user.firstName || user.emailAddresses[0]?.emailAddress}!</span>
            <button 
              className="btn btn-outline-light btn-sm ms-2 me-3" 
              onClick={onLogout}
            >
              Logout
            </button>
          </div>
        )}
      </nav>
    </div>
  );
}

export default Navbar;