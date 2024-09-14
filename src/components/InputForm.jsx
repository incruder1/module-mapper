import React, { useRef, useState } from 'react';
import { IoSend } from 'react-icons/io5';
import Loader from './Loader';
import { useNavigate } from 'react-router-dom';
import './HomePage.scss';

const errorMessages = [
  'Oops, Invalid link or path.',
  "Uh oh, that link doesn't seem to be correct.",
  'Whoops, wrong link! Try again.',
  'Oops, wrong path! Please check your link.',
];

const getRandomErrorMessage = () => {
  return errorMessages[Math.floor(Math.random() * errorMessages.length)];
};

const FormComponent = () => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');

  const handleInputChange = e => {
    setInputValue(e.target.value);
  };

  const handleButtonClick = () => {
    setIsLoading(true);
    console.log(inputValue);
    fetch(`http://localhost:8090/process-all/?dir_path=${inputValue}`)
      .then(response => {
        response.json();
        setIsLoading(false);
        if (response.status === 400) {
          setErrorMessage(getRandomErrorMessage());
        } else {
          console.log('Data fetched successfully');
          navigate('/tree');
        }
      })
      .catch(error => {
        setIsLoading(false);
        console.error('Error fetching data: ', error);
        navigate('/error');
      });
  };

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <div>
          <div class="project-title-div">
            <h1 id="project-title">#Repo_Mapper</h1>
          </div>
          <div className="dir_input_div">
            <input
              type="text"
              className="dir_input"
              placeholder="Github Repo Link / Local File Path"
              value={inputValue}
              onChange={handleInputChange}
            />
            <div className="hit-api-button" onClick={handleButtonClick}>
              <IoSend className="icon-arrow" />
            </div>
          </div>
          <div class="error-msg">{errorMessage}</div>
        </div>
      )}
    </>
  );
};

export default FormComponent;
