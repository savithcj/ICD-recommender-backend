import React from "react";
import ListViewer from "../../Components/ListViewer/ListViewer";
import { connect } from "react-redux";

import * as actions from "../../Store/Actions/index";

const recommendedCodesViewer = props => {
  const recommendedCodesComponentMenuItems = [];
  return (
    <ListViewer
      className="recommendedCodes"
      title="Recommended Codes"
      items={props.recommendedCodes}
      noItemsMessage="No recommendations for the selected codes and age"
      nullItemsMessage="Select codes to get recommendations"
      valueName="rhs"
      descriptionName="description"
      //   acceptItemButton={this.handleAcceptRecommendedCode}
      //   removeItemButton={this.handleRemoveRecommendedCode}
      //   dislikeButton={this.userFlagRuleForReview}
      //   exploreButton={this.handleExploreRecommendedCodeButton}
      allowRearrage={false}
      menuOptions={recommendedCodesComponentMenuItems}
      disableDislikeButtonField="shouldDisableDislikeButton"
      disableTitleGutters={false}
      // button={rejectRemainingRecommendationsButton}
    />
  );
};

const mapStateToProps = state => {
  return {
    recommendedCodes: state.recommended.recommendedCodes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    removeCode: removeCodeIndex => dispatch(actions.removeSelectedCode(removeCodeIndex)),
    setCodes: valueToSet => dispatch(actions.setSelectedCodes(valueToSet))
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(recommendedCodesViewer);
