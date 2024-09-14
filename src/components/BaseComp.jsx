import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Routes } from 'react-router-dom';
import TreeDiag from './TreeDiag';
import MermaidComp from './MermaidComp';
import Button from './ButtonComp'
import Loader from './Loader'


  

const BaseComp = () => {
  const [showMermaid, setShowMermaid] = useState(false);

  const toggleComponent = () => {
    setShowMermaid((prev) => !prev);
  };

  return (

    
    <div style={{ position: 'relative', height: '100vh' }}>
      {showMermaid ? <MermaidComp /> : <TreeDiag />}
      
    <div onClick={toggleComponent}>
    <Button 
      >
      </Button>
    </div>
      
    </div>
  );
};


export default BaseComp;