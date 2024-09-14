import React from 'react';

const ResponsiveCard = () => {
  return (
    <div>
      <h1>Responsive Card</h1>
      <div className="wrapper">
        <div className="card">
          <h3 className="card-title">CARD TITLE</h3>
          <p className="card-content">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.</p>
          <button className="card-btn">READ MORE</button>
        </div>
        <div className="card">
          <h3 className="card-title">CARD TITLE</h3>
          <p className="card-content">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.</p>
          <button className="card-btn">READ MORE</button>
        </div>
        <div className="card">
          <h3 className="card-title">CARD TITLE</h3>
          <p className="card-content">Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.</p>
          <button className="card-btn">READ MORE</button>
        </div>
      </div>
    </div>
  );
};

export default ResponsiveCard;