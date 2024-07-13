import React from 'react';

function Navbar() {
  return (
    <nav className="text-white navbar navbar-dark bg-dark d-flex sawarabi-mincho-regular">
        <div className="flex-grow-1 p-2">PinyImage</div>
        <div className="text-danger p-2 pr-5">Card Search</div>
        <div className="p-2 pr-5">About</div>
        <div className="p-2 pr-5"> </div>
    </nav>
  );
}

export default Navbar;