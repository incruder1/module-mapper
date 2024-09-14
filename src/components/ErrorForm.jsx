import React, { useState } from 'react';
import { IoSend } from "react-icons/io5";
import Loader from './Loader'
import { useNavigate } from 'react-router-dom';
import './HomePage.scss'
import { IoHome } from "react-icons/io5";


const ErrorForm = () => {
const [inputValue, setInputValue] = useState('');
const [isLoading, setIsLoading] = useState(false);
const navigate = useNavigate();

const handleInputChange = (e) => {
    setInputValue(e.target.value);
};

const handleButtonClick = () => {
 navigate('/')
};

return (
    <>
        {isLoading ?  
            <Loader /> :

            <div className='form-error'>
                <div className="form">
                    <h1 className='error-h1'>Error 404</h1>
                    <div className="btn btn__primary btn-error" onClick={handleButtonClick}>
                        <IoHome className="icon-arrow"/>
                    </div>
                </div>
            </div>


        }
    </>
);
};

export default ErrorForm;