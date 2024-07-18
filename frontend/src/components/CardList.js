import React from 'react';
import Card from './Card';
import MasonryGrid from './MasonryGrid';
import '../App.css';

const CardList = ({ cards }) => {
  return (
    <MasonryGrid options={{
      fitWidth: true, horizontalOrder: true
   }}>
      {cards.map((card, index) => (
        <div key={index} className="grid-item">
          <Card {...card} />
        </div>
      ))}
    </MasonryGrid>
  );
};

export default CardList;
