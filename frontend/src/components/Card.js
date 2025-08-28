import React, { useRef } from 'react';
import './Card.css'

const Card = ({ title, pinyin, meaning, con, created, created_display }) => {
    const tiltRef = useRef(null);
    
    // Use the formatted display date if available, otherwise format the ISO date
    const formatDate = (isoDate, displayDate) => {
        if (displayDate) return displayDate;
        if (isoDate) {
            try {
                const date = new Date(isoDate);
                return date.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                });
            } catch (e) {
                return isoDate;
            }
        }
        return 'Unknown date';
    };
    
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
            <span className="badge badge-primary">Added: {formatDate(created, created_display)}</span>
            </div>
        </div>
    );


};
export default Card;