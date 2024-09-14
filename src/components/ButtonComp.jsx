import React from 'react';
import './BaseComp.scss';

import './BaseComp.scss';

class Button extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      buttonText: 'Mermaid View',
      class: '',
    };
  }

  handlePush = e => {
    const buttonText = this.state.buttonText === 'Mermaid View' ? 'Tree View' : 'Mermaid View';
    this.setState({ class: 'loading' }, () => {
      setTimeout(() => {
        this.setState({ class: 'success', buttonText });
      }, 2000);
    });
  };

  render() {
    return (
      <div className="float-button">
        <button onClick={this.handlePush} className={this.state.class}>
          <span>{this.state.buttonText}</span>
        </button>
      </div>
    );
  }
}

export default Button;
