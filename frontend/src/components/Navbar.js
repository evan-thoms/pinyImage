import React from 'react';
import '../App.css'

function Navbar({ onClick, aboutRef, searchRef }) {
  return (<div class="navigation">
    <nav className=" text-white navbar navbar-dark bg-dark d-flex sawarabi-mincho-regular">
        <div className="flex-grow-1 p-2">PinyImage</div>
        <div className="text-danger p-2 pr-5 cursor" onClick={() => onClick(searchRef)}>Card Search</div>
        <div className="p-2 pr-5 cursor" onClick={() => onClick(aboutRef)}>What is PinyImage?</div>
        <div className="p-2 pr-5"> </div>
    </nav>
    </div>
  );
}

export default Navbar;