import React, { useState } from 'react';
import '../App.css';


function CardForm({ onSubmit }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(input);
    setInput('');
  };

  return (
    <div class='cardForm'>
    <form onSubmit={handleSubmit}>
      <label class ="inputLabel" htmlFor="user_input">Input Mandarin Character Here:</label>
      <input
        type="text"
        id="user_input"
        name="user_input"
        class='submit'
        value={input}
        onChange={(e) => setInput(e.target.value)}
        required
      />
      <button class = 'submitButton' type="submit">Get Connections</button>
    </form>
    
    </div>
  );
}

export default CardForm;