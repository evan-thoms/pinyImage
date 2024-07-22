import React, { useState } from 'react';
import '../App.css'

const Search = ({ handleSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
    handleSearch(event.target.value);
  };

  return (
    <div class="cardSearch">
      <div class='searchtext' >
       
          Search for Cards Here:
     
      </div>
      
      <input
        type="text"
        placeholder="Search by Pinyin"
        value={searchTerm}
        class = 'search'
        onChange={handleChange}
        />
    </div>
  );
};

export default Search; 