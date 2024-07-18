import React, { useRef } from 'react';
import './Card.css'

const Card = ({ title, pinyin, meaning, con, created }) => {
    const tiltRef = useRef(null);
    console.log("LOOK HERE", {title}, {pinyin}, {meaning}, {con}, {created})
    return(
        <div data-tilt>
            <div ref={tiltRef} className = "cards">
                <div class="top">
                    <div class="char">
                        <h2 class="text-danger">{title}</h2>
                        <h4 class="pinyin">{pinyin}</h4>
                    </div>
                    <div class='meaning'>
                        <p>{meaning}</p>
                    </div>
                </div>
            <p class="conn">{con}</p>
            <span className="badge badge-primary">Added on: {created}</span>
            </div>
        </div>
    );


};
export default Card;