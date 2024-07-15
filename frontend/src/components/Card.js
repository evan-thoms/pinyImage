import React, { useRef } from 'react';
import './Card.css'

const Card = ({ title, pinyin, def, con, created }) => {
    const tiltRef = useRef(null);
    
    return(
        <div data-tilt>
        <div ref={tiltRef} className = "cards">
                <div class="row">
                    <div class="col-md-auto">
                        <h2 class="text-danger">{title}</h2>
                            <h4 class="pinyin">{pinyin}</h4>
                    </div>
                <div class='col '>
                    <p>{def}</p>
                </div>
                </div>
            <p class="conn">{con}</p>
            <span className="badge badge-primary">Added on: {created}</span>
        </div>
        </div>
    );


};
export default Card;