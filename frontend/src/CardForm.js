import React, { useState } from 'react';

function CardForm({ onSubmit }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="user_input">Input here</label>
      <input
        type="text"
        id="user_input"
        name="user_input"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        required
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default CardForm;