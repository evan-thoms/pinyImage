import React, { useEffect, useRef } from 'react';
import Masonry from 'masonry-layout';
import imagesLoaded from 'imagesloaded';
import './MasonryGrid.css';

const MasonryGrid = ({ children }) => {
    const gridRef = useRef(null);

    useEffect(() => {
        const grid = gridRef.current;
        const masonry = new Masonry(grid, {
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer',
            percentPosition: true,
        });

        imagesLoaded(grid, () => {
            masonry.layout();
        });

        return () => masonry.destroy();
    }, [children]);

    return (
        <div className="grid" ref={gridRef}>
            <div className="grid-sizer"></div>
            {children}
        </div>
    );
};

export default MasonryGrid;
