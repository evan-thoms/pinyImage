import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const  [data, setData] = useState(0);

  useEffect(() => {
    fetch('/api/result', {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => setData(data));

  }, []);
  return (
    <div>
      <h1>React and Flask</h1>
      {data && (
        <>
          <p>{data.result}</p>
          <p>{data.connections}</p>
          <div className="cards">
            {data.cards.map(card => (
              <div key={card.id} className="card">
                <h2>{card.title}</h2>
                <span className="badge badge-primary">{card.created}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
export default App;
