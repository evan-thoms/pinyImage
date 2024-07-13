import React from 'react';

function CardList({ cards }) {
  return (
    <div className="row d-flex justify-content-center">
      {cards.map((card, index) => (
        <div key={index} className="col-md-3 mb-4 bg-highlight">
          <div className="bg-light">
            <h2 class="text-danger">{card.title}</h2>
            <h4>{card.pinyin}</h4>
            <p>{card.content}</p>
            <span className="badge badge-primary">{card.created}</span>
            <hr />
          </div>
        </div>
      ))}
    </div>
  );
}

export default CardList;