import React from 'react';

function CardList({ cards }) {
  return (
    <div className="cards">
      {cards.map((card, index) => (
        <div key={index} className="card">
          <h2>{card.title}</h2>
          <h4>{card.pinyin}</h4>
          <p>{card.content}</p>
          <span className="badge badge-primary">{card.created}</span>
          <hr />
        </div>
      ))}
    </div>
  );
}

export default CardList;