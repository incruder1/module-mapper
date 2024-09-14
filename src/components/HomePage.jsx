import React from "react";
import './HomePage.scss'
import { IoSend } from "react-icons/io5";
import Loader from './Loader'
import { useNavigate } from 'react-router-dom';
import FormComponent from "./InputForm";

class HomePage extends React.Component {
constructor(props){
super(props);

    this.state = {
        droidX: 0,
        mouseX: 0,
        toTheRight: true,
        speed: 2,
        accelMod: 1,
        isLoading: false
    }
}

// Keep track of the mouse position.
handleMouseMove(event) {
    this.setState({
        mouseX: event.pageX
    })
}
handleChange = (e) => {
    this.setState({ inputString: e.target.value });
}

// Speed Mod Bar
handleSpeedChange(e) {
    if(parseFloat(e.target.value)) {
        this.setState({
            speed: e.target.value
        })
    }
}

// Acceleration Mod Bar
handleAccelChange(e) {
    if(parseFloat(e.target.value)) {
        this.setState({
            accelMod: e.target.value
        })
    }
}

// Get moving!
movement() {
    let {droidX, mouseX, speed, accelMod} = this.state;

    if(Math.abs(Math.round(droidX)-mouseX) !== 1){
      
        let distance = mouseX - droidX;
        let acceleration = Math.abs(distance * accelMod) / 100;

        if (droidX < mouseX) {
            this.setState({
                droidX: droidX+(speed*acceleration),
                toTheRight: true
            });
        }
        else {
            this.setState({
                droidX: droidX-(speed*acceleration),
                toTheRight: false
            });
        }
    }
}

// Get some initial movement on first mount. 
componentWillMount() {
    this.setState({
        mouseX: 300
    });
}

// Set up the mouse event listener and fire up the movement function.
componentDidMount() {
    document.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    setInterval(this.movement.bind(this), 1);
}

// Clean up.
componentWillUnmount() {
    document.removeEventListener('mousemove', (e) => this.handleMouseMove(e));
}

handleButtonClick(){
    // this.setState({ isLoading: true });
    console.log(this.inputString)
    fetch('https://localhost:8090/process-all/?dir_path=')
        .then(response => response.json())
        .then(() => {
            console.log("Data fetched successfully");
        })
        .catch(error => {
                console.error("Error fetching data: ", error);
        })

    // navigate('/other-page');
}

render() {
    let {speed, accelMod, droidX, mouseX, toTheRight, isLoading} = this.state;
  
    return (
        <div className="container-home">

            <div className="top-input">
            {isLoading ? 
                <Loader className="loader-top"/> 
                : 
                <FormComponent/>
            }
            </div>

            <div className="bb8" style={{WebkitTransform: `translateX(${droidX}px)`}}>
                <div className={'antennas ' + (toTheRight ? 'right' : '')}
                     style={{WebkitTransform: `translateX(${(mouseX - droidX) / 25}px) rotateZ(${(mouseX - droidX) / 80 }deg)`}}>
                    <div className="antenna short"></div>
                    <div className="antenna long"></div>
                </div>
                <div className="head"
                     style={{WebkitTransform: `translateX(${(mouseX - droidX) / 15}px) rotateZ(${(mouseX - droidX) / 25}deg)`}}>
                    <div className="stripe one"></div>
                    <div className="stripe two"></div>
                    <div className={'eyes ' + (toTheRight ? 'right' : '')}>
                        <div className="eye one"></div>
                        <div className="eye two"></div>
                    </div>
                    <div className={'stripe detail ' + (toTheRight ? 'right' : '')}>
                        <div className="detail zero"></div>
                        <div className="detail zero"></div>
                        <div className="detail one"></div>
                        <div className="detail two"></div>
                        <div className="detail three"></div>
                        <div className="detail four"></div>
                        <div className="detail five"></div>
                        <div className="detail five"></div>
                    </div>
                    <div className="stripe three"></div>
                </div>
                <div className="ball" style={{WebkitTransform: `rotateZ(${droidX / 2}deg)`}}>
                    <div className="lines one"></div>
                    <div className="lines two"></div>
                    <div className="ring one"></div>
                    <div className="ring two"></div>
                    <div className="ring three"></div>
                </div>
                <div className="shadow"></div>
            </div>
        </div>
    );
}
}

export default HomePage;