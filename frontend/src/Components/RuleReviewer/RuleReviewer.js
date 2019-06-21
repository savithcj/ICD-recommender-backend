import React, { useState, useEffect } from "react";
import ListViewer from "../../Components/ListViewer/ListViewer";

import APIClass from "./../../Model/API";

export default function RuleReviewer() {
  const [flaggedRules, setFlaggedRules] = useState([]);

  useEffect(() => {
    getFlaggedRulesFromAPI();
  }, []);

  const getFlaggedRulesFromAPI = () => {
    const url = APIClass.getAPIURL("FLAGGED_RULES") + "?format=json";

    fetch(url)
      .then(response => response.json())
      .then(results => {
        results.forEach(ruleObject => {
          ruleObject.rule = ruleObject.lhs + " \u2192 " + ruleObject.rhs;
        });
        setFlaggedRules(results);
      });
  };

  const handleAcceptRule = event => {
    const acceptRuleIndex = parseInt(event.currentTarget.id, 10);

    const url = APIClass.getAPIURL("UPDATE_FLAGGED_RULES") + flaggedRules[acceptRuleIndex].id + ",ACCEPT/";

    const rules = [...flaggedRules];

    //ListViewer will display a loading indicator while the API promise is being fullfilled
    setFlaggedRules("LOADING");

    fetch(url, { method: "PUT" }).then(response => {
      console.log(response.status);
      //Only removes a rule from the list viewer if the put request was successful
      //TODO: show a message to the user if the request failed
      if (response.status === 200) {
        rules.splice(acceptRuleIndex, 1);
      }
      setFlaggedRules(rules);
    });
  };

  const handleRejectRule = event => {
    const rejectRuleIndex = parseInt(event.currentTarget.id, 10);

    const url = APIClass.getAPIURL("UPDATE_FLAGGED_RULES") + flaggedRules[rejectRuleIndex].id + ",REJECT/";

    const rules = [...flaggedRules];

    setFlaggedRules("LOADING");

    fetch(url, { method: "PUT" }).then(response => {
      console.log(response.status);
      //Only removes a rule from the list viewer if the put request was successful
      //TODO: show a message to the user if the request failed
      if (response.status === 200) {
        rules.splice(rejectRuleIndex, 1);
      }
      setFlaggedRules(rules);
    });
  };

  return (
    <div className="grid-block">
      <ListViewer
        className="ruleReviwer"
        title="List of flagged rules"
        items={flaggedRules}
        noItemsMessage="No flagged rules"
        valueName="rule"
        descriptionName="description"
        acceptItemButton={handleAcceptRule}
        removeItemButton={handleRejectRule}
        allowRearrage={false}
        menuOptions={[]}
        disableTitleGutters={true}
      />
    </div>
  );
}
