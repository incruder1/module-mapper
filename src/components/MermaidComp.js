import React from 'react';
import ReactDOM from 'react-dom';
import Mermaid from './Mermaid';
// import example from '../examples/ExampleMermaid';
import './mermaid.css';
import example from '../auto-gen/mermaid_code/graph'
function MermaidComp() {
  console.log(example);
  return (
    <div className="merm">
      <div className="main-title">Mermaid Diagram</div>
      <Mermaid chart={example} />
    </div>
  );
}
export default MermaidComp;
