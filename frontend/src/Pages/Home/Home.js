import React, { useState, useEffect } from "react";
import InputBoxes from "../../Containers/InputBoxes/InputBoxes";
import SelectedCodes from "../../Containers/SelectedCodes/SelectedCodes";
import RecommendedCodes from "../../Containers/RecommendedCodes/RecommendedCodes";
import DaggerAsterisks from "../../Containers/DaggerAsterisks/DaggerAsterisks";
import TreeViewer from "../../Containers/TreeViewer/TreeViewer";
import MenuBar from "../../Containers/MenuBar/MenuBar";
import { getFromLS, saveToLS } from "../../Util/layoutFunctions";
import { defaultLayouts } from "./layouts";
import { WidthProvider, Responsive } from "react-grid-layout";
import * as actions from "../../Store/Actions/index";
import { connect } from "react-redux";
import "./Home.css";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";

const ResponsiveReactGridLayout = WidthProvider(Responsive);
const originalLayouts = getFromLS("homeLayouts", "layouts") || defaultLayouts;
const treeViewDiv = React.createRef();
const Home = props => {
  //Local state of the Home page

  const [layouts, setLayouts] = useState(JSON.parse(JSON.stringify(originalLayouts)));
  const [isLayoutModifiable, setLayoutModifiable] = useState(false);

  //this useEffect is equivalent to the componentWillUnmount lifecycle method
  useEffect(() => {
    return () => {
      console.log("[Home Page] useEffect called");
      props.resetState();
    };
  }, []);

  const resetLayout = () => {
    setLayouts(defaultLayouts);
    saveToLS("homeLayouts", "layouts", defaultLayouts);
  };

  function handleLayoutModifierButton() {
    const layoutModifiable = !isLayoutModifiable;
    setLayoutModifiable(layoutModifiable);
  }

  function onLayoutChange(layouts) {
    setLayouts(layouts);
    console.log("in onlayoutchange");
    saveToLS("homeLayouts", "layouts", layouts);
  }

  function handleTreeChange() {
    if (treeViewDiv.current !== null) {
      treeViewDiv.current.handleResize();
    }
  }

  const highlightEditDiv = isLayoutModifiable ? "grid-border edit-border" : "grid-border";

  return (
    <div className="Home">
      <MenuBar
        title="ICD-10 Code Suggestion and Usage Insight"
        firstLinkName="Admin"
        firstLinkRoute="/admin"
        secondLinkName="Visualization"
        secondLinkRoute="/visualization"
        handleLayoutConfirm={() => handleLayoutModifierButton()}
        handleResetLayout={resetLayout}
        inModifyMode={isLayoutModifiable}
      />
      <ResponsiveReactGridLayout
        className="layout"
        rowHeight={10}
        cols={{ lg: 48, md: 40, sm: 24, xs: 16, xxs: 8 }}
        layouts={layouts}
        draggableCancel="input,textarea"
        isDraggable={isLayoutModifiable} //used to dynamically allow editing
        isResizable={isLayoutModifiable} //if a button is pressed
        onLayoutChange={(layout, layouts) => onLayoutChange(layouts)}
      >
        <div key="tree" className={highlightEditDiv}>
          <TreeViewer ref={treeViewDiv} onChange={handleTreeChange()} />
        </div>

        <div key="selectedCodes" className={highlightEditDiv}>
          <SelectedCodes treeRef={treeViewDiv} />
        </div>

        <div key="recommendedCodes" className={highlightEditDiv}>
          <RecommendedCodes treeRef={treeViewDiv} />
        </div>

        <div key="daggerCodes" className={highlightEditDiv}>
          <DaggerAsterisks treeRef={treeViewDiv} />
        </div>

        <div key="inputBoxes" className={highlightEditDiv}>
          <InputBoxes />
        </div>
      </ResponsiveReactGridLayout>
    </div>
  );
};

const mapDispatchToProps = dispatch => {
  return {
    resetState: () => dispatch(actions.resetState())
  };
};

export default connect(
  null,
  mapDispatchToProps
)(Home);