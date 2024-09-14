import React from 'react';
import './Loader.css';
const Loader = () => {
  return (
    <main>
      <div
        className="preloader"
        style={{
          position: 'absolute',
          left: '20%',
          top: '20%',
          backgroundColor: '#303134',
          '--shade1': '#666',
          '--shade4': '#aaa',
        }}
      >
        <div
          className="preloader__square"
          style={{ backgroundColor: '#88D66C', '--shade1': '#B4E380', '--shade4': '#B4E380' }}
        ></div>
        <div
          className="preloader__square"
          style={{ backgroundColor: '#D20062', '--shade1': '#D6589F', '--shade4': '#D6589F' }}
        ></div>
        <div
          className="preloader__square"
          style={{ backgroundColor: '#FFB22C', '--shade1': '#FFDE4D', '--shade4': '#FFDE4D' }}
        ></div>
        <div
          className="preloader__square"
          style={{ backgroundColor: '#5A639C', '--shade1': '#E2BBE9', '--shade4': '#E2BBE9' }}
        ></div>
      </div>
      <div className="status"></div>
    </main>
  );
};

export default Loader;
