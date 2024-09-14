import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import BaseComp from './components/BaseComp'
import Error from './components/Error'

const App = () => {
  return (
    <Router>
        <Routes>
          <Route exact path="/" element={<HomePage />} />
          <Route path="/tree" element={<BaseComp />} />
          <Route path="/error" element={<Error />} />
          <Route path="*" element={<Error />} />

        </Routes>
    </Router>
  );
};

export default App;