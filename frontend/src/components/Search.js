import React, { useState } from 'react';

const Search = ({ handleSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
    handleSearch(event.target.value);
  };

  return (
    <div className="d-flex justify-content-center">
      <div >
        <h2>
          Search for Cards Here
          </h2>
      </div>
      
      <input
        type="text"
        placeholder="Search by Character Pinyin"
        value={searchTerm}
        onChange={handleChange}
        />
    </div>
  );
};

export default Search;


// *For example purposes, the pinyImage uses a rudimentary free api. The example cards below may provide more useful mental images, as they were generated with ChatGPT