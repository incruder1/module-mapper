import React, { Component } from 'react';
import clone from 'clone';
import Tree from 'react-d3-tree';
import Switch from './Switch';
import MixedNodeElement from './MixedNodeElement';
import PureSvgNodeElement from './PureSvgNodeElement';
import './TreeDiag.scss';
import { IconName } from 'react-icons/ai';
import { AiOutlineZoomIn, AiOutlineZoomOut } from 'react-icons/ai';

// Data examples
import mapJson from '../auto-gen/antd_data.json';

console.log('Demo React version: ', React.version);

const customNodeFnMapping = {
  svg: {
    description: 'Tree Diagram',
    fn: (rd3tProps, appState) => (
      <PureSvgNodeElement
        nodeDatum={rd3tProps.nodeDatum}
        toggleNode={rd3tProps.toggleNode}
        orientation={appState.orientation}
      />
    ),
  },
  mixed: {
    description: 'Block Diagram',
    fn: ({ nodeDatum, toggleNode }, appState) => (
      <MixedNodeElement
        nodeData={nodeDatum}
        triggerNodeToggle={toggleNode}
        foreignObjectProps={{
          width: 500,
          height: 500,
          x: 50,
          y: 20,
        }}
      />
    ),
  },
};

const countNodes = (count = 0, n) => {
  // Count the current node
  count += 1;

  // Base case: reached a leaf node.
  if (!n.children) {
    return count;
  }

  // Keep traversing children while updating `count` until we reach the base case.
  return n.children.reduce((sum, child) => countNodes(sum, child), count);
};

class TreeDiag extends Component {
  constructor() {
    super();

    this.addedNodesCount = 0;

    this.state = {
      data: mapJson,
      totalNodeCount: countNodes(0, Array.isArray(mapJson) ? mapJson[0] : mapJson),
      orientation: 'horizontal',
      dimensions: undefined,
      centeringTransitionDuration: 600,
      translateX: 300,
      translateY: 300,
      collapsible: true,
      shouldCollapseNeighborNodes: true,
      initialDepth: 1,
      depthFactor: undefined,
      zoomable: true,
      draggable: true,
      zoom: 0.65,
      scaleExtent: { min: 0.1, max: 1 },
      separation: { siblings: 0.5, nonSiblings: 1 },
      nodeSize: { x: 500, y: 280 },
      enableLegacyTransitions: true,
      transitionDuration: 300,
      renderCustomNodeElement: customNodeFnMapping['mixed'].fn,
      styles: {
        nodes: {
          node: {
            circle: {
              fill: '#52e2c5',
            },
            attributes: {
              stroke: '#000',
            },
          },
          leafNode: {
            circle: {
              // fill: '#800000',
            },
            attributes: {
              // stroke: '#800000',
            },
          },
        },
      },
    };

    this.setTreeData = this.setTreeData.bind(this);
    this.setLargeTree = this.setLargeTree.bind(this);
    this.setOrientation = this.setOrientation.bind(this);
    this.setPathFunc = this.setPathFunc.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleFloatChange = this.handleFloatChange.bind(this);
    this.toggleCollapsible = this.toggleCollapsible.bind(this);
    this.toggleZoomable = this.toggleZoomable.bind(this);
    this.toggleDraggable = this.toggleDraggable.bind(this);
    this.toggleCenterNodes = this.toggleCenterNodes.bind(this);
    this.setScaleExtent = this.setScaleExtent.bind(this);
    this.setSeparation = this.setSeparation.bind(this);
    this.setNodeSize = this.setNodeSize.bind(this);
  }

  setTreeData(data) {
    this.setState({
      data,
      totalNodeCount: countNodes(0, Array.isArray(data) ? data[0] : data),
    });
  }

  setLargeTree(data) {
    this.setState({
      data,
      transitionDuration: 0,
    });
  }

  setOrientation(orientation) {
    this.setState({ orientation });
  }

  setPathFunc(pathFunc) {
    this.setState({ pathFunc });
  }
  handleZoomIn = () => {
    this.setState(prevState => {
      if (prevState.zoom < 1) {
        return { zoom: prevState.zoom + 0.1 };
      }
      return null;
    });
  };

  handleZoomOut = () => {
    this.setState(prevState => {
      if (prevState.zoom > 0) {
        return { zoom: prevState.zoom - 0.1 };
      }
      return null;
    });
  };
  handleChange(evt) {
    const target = evt.target;
    const parsedIntValue = parseInt(target.value, 10);
    if (target.value === '') {
      this.setState({
        [target.name]: undefined,
      });
    } else if (!isNaN(parsedIntValue)) {
      this.setState({
        [target.name]: parsedIntValue,
      });
    }
  }

  handleFloatChange(evt) {
    const target = evt.target;
    const parsedFloatValue = parseFloat(target.value);
    if (target.value === '') {
      this.setState({
        [target.name]: undefined,
      });
    } else if (!isNaN(parsedFloatValue)) {
      this.setState({
        [target.name]: parsedFloatValue,
      });
    }
  }

  handleCustomNodeFnChange = evt => {
    const customNodeKey = evt.target.value;

    this.setState({ renderCustomNodeElement: customNodeFnMapping[customNodeKey].fn });
  };

  toggleCollapsible() {
    this.setState(prevState => ({ collapsible: !prevState.collapsible }));
  }

  toggleCollapseNeighborNodes = () => {
    this.setState(prevState => ({
      shouldCollapseNeighborNodes: !prevState.shouldCollapseNeighborNodes,
    }));
  };

  toggleZoomable() {
    this.setState(prevState => ({ zoomable: !prevState.zoomable }));
  }

  toggleDraggable() {
    this.setState(prevState => ({ draggable: !prevState.draggable }));
  }

  toggleCenterNodes() {
    if (this.state.dimensions !== undefined) {
      this.setState({
        dimensions: undefined,
      });
    } else {
      if (this.treeContainer) {
        const { width, height } = this.treeContainer.getBoundingClientRect();
        this.setState({
          dimensions: {
            width,
            height,
          },
        });
      }
    }
  }

  setScaleExtent(scaleExtent) {
    this.setState({ scaleExtent });
  }

  setSeparation(separation) {
    if (!isNaN(separation.siblings) && !isNaN(separation.nonSiblings)) {
      this.setState({ separation });
    }
  }

  setNodeSize(nodeSize) {
    if (!isNaN(nodeSize.x) && !isNaN(nodeSize.y)) {
      this.setState({ nodeSize });
    }
  }

  addChildNode = () => {
    const data = clone(this.state.data);
    const target = data[0].children ? data[0].children : data[0]._children;
    this.addedNodesCount++;
    target.push({
      name: `Inserted Node ${this.addedNodesCount}`,
      id: `inserted-node-${this.addedNodesCount}`,
    });
    this.setState({
      data,
    });
  };

  removeChildNode = () => {
    const data = clone(this.state.data);
    const target = data[0].children ? data[0].children : data[0]._children;
    target.pop();
    this.addedNodesCount--;
    this.setState({
      data,
    });
  };

  componentDidMount() {
    const dimensions = this.treeContainer.getBoundingClientRect();
    this.setState({
      translateX: dimensions.width / 2.5,
      translateY: dimensions.height / 2,
    });
  }

  render() {
    return (
      <div className="reset-this">
        <div className="column-left">
          <div className="controls-container">
            <div className="prop-container">
              <h4 className="prop">Orientation</h4>

              <div className="button-combo">
                <div
                  className="btn btn__primary btn_tree"
                  onClick={() => this.setOrientation('horizontal')}
                >
                  <p>{'HORIZONTAL'}</p>
                </div>
                <div
                  className="btn btn__primary btn_tree"
                  onClick={() => this.setOrientation('vertical')}
                >
                  <p>{'VERTICAL'}</p>
                </div>
              </div>
            </div>

            <div className="prop-container">
              <h4 className="prop">Path style</h4>

              <div className="button-combo">
                <div
                  className="btn btn__primary btn_tree"
                  onClick={() => this.setPathFunc('diagonal')}
                >
                  <p>{'DIAGONAL'}</p>
                </div>
                <div
                  className="btn btn__primary btn_tree"
                  onClick={() => this.setPathFunc('elbow')}
                >
                  <p>{'ELBOW'}</p>
                </div>
              </div>

              <div className="button-combo">
                <div
                  className="btn btn__primary btn_tree"
                  onClick={() => this.setPathFunc('straight')}
                >
                  <p>{'STRAIGHT'}</p>
                </div>
                <div className="btn btn__primary btn_tree" onClick={() => this.setPathFunc('step')}>
                  <p>{'STEP'}</p>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex' }} className="switch-div-1">
              <div className="prop-container switches">
                <h4 className="prop">Collapsible</h4>
                <Switch
                  name="collapsibleBtn"
                  checked={this.state.collapsible}
                  onChange={this.toggleCollapsible}
                />
              </div>

              <div className="prop-container switches">
                <h4 className="prop">Zoomable</h4>
                <Switch
                  name="zoomableBtn"
                  checked={this.state.zoomable}
                  onChange={this.toggleZoomable}
                />
              </div>
            </div>

            <div style={{ display: 'flex' }} className="switch-div-2">
              <div className="prop-container switches">
                <h4 className="prop">Center Nodes</h4>
                <Switch
                  name="centerNodesBtn"
                  checked={this.state.dimensions !== undefined}
                  onChange={this.toggleCenterNodes}
                />
              </div>

              <div className="prop-container switches">
                <h4 className="prop">Collapse Neighbour</h4>
                <Switch
                  name="collapseNeighborsBtn"
                  checked={this.state.shouldCollapseNeighborNodes}
                  onChange={this.toggleCollapseNeighborNodes}
                />
              </div>
            </div>

            <div className="prop-container zoom-btns-div">
              <div className="button-combo">
                <div className="btn btn__primary btn_tree" onClick={this.handleZoomIn}>
                  <p>
                    <AiOutlineZoomIn style={{ fontSize: '24px', marginTop: '2px' }} />
                  </p>
                </div>
                <div className="btn btn__primary btn_tree" onClick={this.handleZoomOut}>
                  <p>
                    <AiOutlineZoomOut style={{ fontSize: '24px' }} />
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="demo-container">
          <div className="column-right">
            <div
              className="tree-stats-container"
              style={{
                float: 'right',
                height: '0px',
                color: '#424242',
                textTransform: 'uppercase',
              }}
            >
              Total nodes: {this.state.totalNodeCount}
            </div>
            <div ref={tc => (this.treeContainer = tc)} className="tree-container">
              <Tree
                hasInteractiveNodes
                data={this.state.data}
                renderCustomNodeElement={
                  this.state.renderCustomNodeElement
                    ? rd3tProps => this.state.renderCustomNodeElement(rd3tProps, this.state)
                    : undefined
                }
                rootNodeClassName="demo-node"
                branchNodeClassName="demo-node"
                orientation={this.state.orientation}
                dimensions={this.state.dimensions}
                centeringTransitionDuration={this.state.centeringTransitionDuration}
                translate={{ x: this.state.translateX, y: this.state.translateY }}
                pathFunc={this.state.pathFunc}
                collapsible={this.state.collapsible}
                initialDepth={this.state.initialDepth}
                zoomable={this.state.zoomable}
                draggable={this.state.draggable}
                zoom={this.state.zoom}
                scaleExtent={this.state.scaleExtent}
                nodeSize={this.state.nodeSize}
                separation={this.state.separation}
                enableLegacyTransitions={this.state.enableLegacyTransitions}
                transitionDuration={this.state.transitionDuration}
                depthFactor={this.state.depthFactor}
                styles={this.state.styles}
                shouldCollapseNeighborNodes={this.state.shouldCollapseNeighborNodes}
                // onUpdate={(...args) => {console.log(args)}}
                onNodeClick={(node, evt) => {
                  console.log('onNodeClick', node, evt);
                }}
                onNodeMouseOver={(...args) => {
                  console.log('onNodeMouseOver', args);
                }}
                onNodeMouseOut={(...args) => {
                  console.log('onNodeMouseOut', args);
                }}
                onLinkClick={(...args) => {
                  console.log('onLinkClick');
                  console.log(args);
                }}
                onLinkMouseOver={(...args) => {
                  console.log('onLinkMouseOver', args);
                }}
                onLinkMouseOut={(...args) => {
                  console.log('onLinkMouseOut', args);
                }}
              />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default TreeDiag;
