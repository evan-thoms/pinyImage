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
            horizontalOrder: true,
        });

        imagesLoaded(grid, () => {
            masonry.layout();
        });

        const handleResize = () => {
            masonry.layout();
          };
      
          window.addEventListener('resize', handleResize);

        return () => {
            masonry.destroy();
            window.removeEventListener('resize', handleResize);
        };
    }, [children]);

    return (
        <div className="grid" ref={gridRef}>
            <div className="grid-sizer"></div>
            {children}
        </div>
    );
};

export default MasonryGrid;
