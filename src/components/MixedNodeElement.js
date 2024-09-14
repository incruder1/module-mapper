import React, { useState, useRef } from 'react';
import { Space, Card } from 'antd';
import { AiFillEnvironment } from "react-icons/ai";
import ResponsiveCard from './Card';


const CardComp = ({nodeData={}}) => (
  // <Space direction="vertical" size={16} style={{color: "white"}}>
    <Card titleStyle={{ background: '#ff0000' , color: "white"}}
      hoverable
      title={<span style={{color: "white"}}>{nodeData.attributes.Type}</span>}
      extra={<span style={{color: "white"}}>{nodeData.name}</span>}
      style={{
        height: 300,
        width: 400,
        backgroundColor: 'Blue',
        color: 'black',
        overflow: 'hidden',
        color: "black",
        position: 'relative',
        display: 'inline-block',

      }}
    >
            <ul style={{ listStyleType: 'none', padding: 0 }}>
              {nodeData.attributes &&
                Object.keys(nodeData.attributes).map((labelKey, i) => (
                  <li key={`${labelKey}-${i}`}>
                    {labelKey}: {nodeData.attributes[labelKey]}
                  </li>
                ))}
            </ul>
    </Card>
);

const MixedNodeElement = ({ nodeData = {}, triggerNodeToggle, foreignObjectProps = {} }) => {
  const [isHovering, setIsHovering] = useState(false);
  const timerRef = useRef(null);

  const handleCircleHover = (hovering) => {
    setIsHovering(hovering);
    if (hovering) {
      clearTimeout(timerRef.current);
    }
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
    // timerRef.current = setTimeout(() => {
    //   setIsHovering(false);
    // }, 5000);
  };

  return (
    <React.Fragment>
      <circle style={{zIndex: -200}}
        r={25}
        onMouseEnter={() => handleCircleHover(true)}
        onMouseLeave={handleMouseLeave}
        onClick={triggerNodeToggle}
      >
      </circle>

      {/* {isHovering} ?<text style={{color: "#444"}}>{nodeData.name}</text> : <text style={{color: "#444"}}></text> */}

    
      {/* <foreignObject  width={400} height={600} x={+40} y={-50}>
              {isHovering ? <CardComp nodeData={nodeData} />: <></>} 
              
      </foreignObject> */}

      <foreignObject width={400} height={500} x={-100} y={20} >
            {/* <h6 style={{color: "#444", fontWeight: 500, fontSize:  "20px",display: "inline-block",width: "auto", backgroundColor: 'white' }}>{nodeData.name}</h6>               */}
            <div style={{color: "#444", fontWeight: 500, fontSize:  "20px" }}>{nodeData.name}</div>              
      </foreignObject>

      
    </React.Fragment>
  );
};

export default MixedNodeElement;