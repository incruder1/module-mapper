import React from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose',
  themeCSS: `
    g.classGroup rect {
      fill: #282a36;
      stroke: #6272a4;
    } 
    g.classGroup text {
      fill: #f8f8f2;
    }
    g.classGroup line {
      stroke: #f8f8f2;
      stroke-width: 0.5;
    }
    .classLabel .box {
      stroke: #21222c;
      stroke-width: 3;
      fill: #21222c;
      opacity: 1;
    }
    .classLabel .label {
      fill: #f1fa8c;
    }

    span.nodeLabel {
		color: #EAEAEA;                      # all text colors
		font-size: 14px;
		font-weight: 400;
	}

	.classTitle .nodeLabel {
		font-weight: 500;
		font-size: 15px;
		color: #F6995C;
	}
      
    rect.outer.title-state {
      fill: #31363F;                     # box background-color
      border-color: white;                
      stroke: #FF165D;                   # box border color
	  }

	rect.outer.title-state {
		stroke-width: 2px;
	}

	.divider {
        stroke: #FF165D;                   # innerLines color
        box-shadow: 10px;
    }

	.divider {
		stroke-width: 1px;
    }
	

    rect {
      rx: 5;                            # box radius
    }

    .relation {
      stroke: #FF165D;                     # arrow color
      stroke-width: 1;
    }
	  
    .edgeLabels .edgeLabel {
      color: #000;                    # Label color
      fill: black;
      font-size: 16px;
	  font-weight: 500;
    }
    span.edgeLabel > span.edgeLabel {
       background-color: #51EAEA	;            # Label bg color
	   display: block-inline;
	   border-radius: 5px;
	   padding: 10px 10px;
    }

    #compositionStart, #compositionEnd {
      fill: #bd93f9;
      stroke: #bd93f9;
      stroke-width: 1;
    }
    #aggregationEnd, #aggregationStart {
      fill: #21222c;
      stroke: #50fa7b;
      stroke-width: 1;
    }
    #dependencyStart, #dependencyEnd {
      fill: #00bcd4;
      stroke: #00bcd4;
      stroke-width: 1;
    } 
    #extensionStart, #extensionEnd {
      fill: #f8f8f2;
      stroke: #f8f8f2;
      stroke-width: 1;
    }`,
  fontFamily: 'Fira Code',
});

export default class Mermaid extends React.Component {
  componentDidMount() {
    mermaid.contentLoaded();
  }
  render() {
    return <div className="mermaid">{this.props.chart}</div>;
  }
}
