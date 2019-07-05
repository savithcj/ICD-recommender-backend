import React from "react";
import ListViewer from "../../Components/ListViewer/ListViewer";
import { connect } from "react-redux";
import * as actions from "../../Store/Actions/index";

const selectedCodesViewer = props => {
  const handleRemoveSelectedCode = event => {
    const selectedCodes = Array.from(props.selectedCodes);
    const removeCodeIndex = parseInt(event.currentTarget.id, 10);
    selectedCodes.splice(removeCodeIndex, 1);
    props.removeSelectedCode(removeCodeIndex);
    props.getRecommendedCodes(selectedCodes);
    props.getDaggerAsterisks(selectedCodes);
  };

  const handleExploreSelectedCodeButton = event => {
    const exploreCodeIndex = parseInt(event.currentTarget.id, 10);
    props.treeRef.current.changeTree(props.selectedCodes[exploreCodeIndex].code);
  };

  const resetSelectedCodes = () => {
    props.setSelectedCodes([]);
    props.setRecommendedCodes(null);
    props.setDaggerAsterisk(null);
  };

  const acceptSelectedCodes = () => {
    //TODO:Make API call to update code usage during a session
    resetSelectedCodes();
  };

  const selectedCodesComponentMenuItems = [
    {
      menuItemOnClick: props.selectedCodes.length < 2 ? null : resetSelectedCodes,
      menuItemText: "Remove All Items"
    }
  ];

  const acceptSelectedCodesButton = {
    text: "Accept",
    onClick: acceptSelectedCodes,
    title: "Accept all selected codes"
  };

  return (
    <ListViewer
      title="Selected Codes"
      items={props.selectedCodes}
      noItemsMessage="No codes selected"
      valueName="code"
      descriptionName="description"
      removeItemButton={handleRemoveSelectedCode}
      exploreButton={handleExploreSelectedCodeButton}
      onSortEndCallback={updatedListOfSelectedCodes => {
        props.setSelectedCodes(updatedListOfSelectedCodes);
      }}
      allowRearrage={props.selectedCodes.length > 1}
      menuOptions={selectedCodesComponentMenuItems}
      button={props.selectedCodes.length > 0 ? acceptSelectedCodesButton : null}
      disableTitleGutters={false}
    />
  );
};

const mapStateToProps = state => {
  return {
    selectedCodes: state.selected.selectedCodes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    removeSelectedCode: removeCodeIndex => dispatch(actions.removeSelectedCode(removeCodeIndex)),
    setSelectedCodes: valueToSet => dispatch(actions.setSelectedCodes(valueToSet)),
    getRecommendedCodes: (codeObjArray, age, gender) =>
      dispatch(actions.fetchRecommendationsAndUpdateCache(codeObjArray, age, gender)),
    getDaggerAsterisks: codeObjArray => dispatch(actions.fetchDaggerAsterisksAndUpdateCache(codeObjArray)),
    setRecommendedCodes: valueToSet => dispatch(actions.setRecommendedCodes(valueToSet)),
    setDaggerAsterisk: valueToSet => dispatch(actions.setDaggerAsterisk(valueToSet))
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(selectedCodesViewer);