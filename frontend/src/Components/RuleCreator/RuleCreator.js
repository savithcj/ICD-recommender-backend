import React, { useState } from "react";
import CodeInputField from "../../Components/CodeInputField/CodeInputField";
import ListViewer from "../../Components/ListViewer/ClassBasedListViewer";
import "./RuleCreator.css";

function RuleCreator(props) {
  const [codeAutoCompleteDisplayed, setCodeAutoCompleteDisplayed] = useState([]);
  const [cachedCodeWithDescription, setCachedCodes] = useState([]);
  const [LHS, setLHS] = useState([]);
  const [RHS, setRHS] = useState([]);
  const [ageStart, setAgeStart] = useState();
  const [ageEnd, setAgeEnd] = useState();
  const [gender, setGender] = useState();

  const addCodeLHS = newCodeObj => {
    let selectedCodes = Array.from(LHS);
    // check if the code already exist in the selection
    const getDuplicate = selectedCodes.find(codeObj => codeObj.code === newCodeObj);
    if (getDuplicate === undefined) {
      // get code description from auto-suggest cache
      const codeDescriptions = Array.from(cachedCodeWithDescription);
      const cachedCode = codeDescriptions.find(codeObj => codeObj.code === newCodeObj);
      // construct new code object
      const newCode = {
        code: cachedCode.code,
        description: cachedCode.description
      };
      selectedCodes.push(newCode);
      setLHS(selectedCodes);
    }
  };

  const addCodeRHS = newCodeObj => {
    let selectedCodes = Array.from(RHS);
    // check if the code already exist in the selection
    const getDuplicate = selectedCodes.find(codeObj => codeObj.code === newCodeObj);
    if (getDuplicate === undefined) {
      // get code description from auto-suggest cache
      const codeDescriptions = Array.from(cachedCodeWithDescription);
      const cachedCode = codeDescriptions.find(codeObj => codeObj.code === newCodeObj);
      // construct new code object
      const newCode = {
        code: cachedCode.code,
        description: cachedCode.description
      };
      selectedCodes.push(newCode);
      setRHS(selectedCodes);
    }
  };

  const addAgeStart = value => {
    setAgeStart(value);
  };
  const addAgeEnd = value => {
    setAgeEnd(value);
  };
  const addGender = value => {
    setGender(value);
  };

  /**
   *  Required for code searchbox Auto-Complete
   * Cache code suggestion results from API call to state for repeated quiries
   * Updates the cachedCodeList and cachedCodeWithDescription in App.state
   * @param {*} results
   * @param {*} oFunc optional function to be called at end of the method
   * @param {*} oArg optinal argument for the optional function
   */

  const appendCodeToCache = results => {
    let codesWithDescript = Array.from(cachedCodeWithDescription);

    for (let i = 0, l = results.length; i < l; i++) {
      let thisCode = results[i];
      let codeFound = codesWithDescript.find(codeObj => codeObj.code === thisCode.code);
      if (codeFound === undefined) {
        codesWithDescript.push(thisCode);
      }
    }

    setCachedCodes(codesWithDescript);
  };

  const resetLHSCodes = () => {
    setLHS([]);
  };

  const handleRemoveLHSCode = event => {
    const removeCodeIndex = parseInt(event.currentTarget.id, 10);
    const codes = [...LHS];
    codes.splice(removeCodeIndex, 1);
    setLHS(codes);
  };

  const handleRemoveRHSCode = event => {
    const removeCodeIndex = parseInt(event.currentTarget.id, 10);
    const codes = [...RHS];
    codes.splice(removeCodeIndex, 1);
    setRHS(codes);
  };

  const resetRHSCodes = () => {
    setRHS([]);
  };

  const exploreCodeDetail = code => {};

  const LHSCodesComponentMenuItems = [
    {
      menuItemOnClick: LHS.length > 1 ? resetLHSCodes : null,
      menuItemText: "Remove All Items"
    }
  ];

  const RHSCodesComponentMenuItems = [
    {
      menuItemOnClick: RHS.length > 1 ? resetRHSCodes : null,
      menuItemText: "Remove All Items"
    }
  ];

  return (
    <div>
      <div>
        <div>
          <ListViewer
            title="LHS Codes"
            items={LHS}
            noItemsMessage="No codes selected"
            valueName="code"
            descriptionName="description"
            removeItemButton={handleRemoveLHSCode}
            exploreButton={exploreCodeDetail}
            onSortEndCallback={updatedListOfSelectedCodes => {
              setLHS({ updatedListOfSelectedCodes });
            }}
            allowRearrage={false}
            menuOptions={LHSCodesComponentMenuItems}
          />
        </div>
        <div>
          <CodeInputField
            id_code="inputCodeLHS"
            placeholder_code="LHS Code"
            selectCode={addCodeLHS}
            codeCache={cachedCodeWithDescription}
            appendCodeToCache={appendCodeToCache}
            autoClearCode={true}
          />
        </div>
      </div>
      <div>
        <div>
          <ListViewer
            title="RHS Codes"
            items={RHS}
            noItemsMessage="No codes selected"
            valueName="code"
            descriptionName="description"
            removeItemButton={handleRemoveRHSCode}
            exploreButton={exploreCodeDetail}
            onSortEndCallback={updatedListOfSelectedCodes => {
              setRHS({ updatedListOfSelectedCodes });
            }}
            allowRearrage={false}
            menuOptions={RHSCodesComponentMenuItems}
          />
        </div>
        <div>
          <CodeInputField
            id_code="inputCodeRHS"
            placeholder_code="RHS Code"
            selectCode={addCodeRHS}
            codeCache={cachedCodeWithDescription}
            appendCodeToCache={appendCodeToCache}
            autoClearCode={true}
          />
        </div>
      </div>
      <div>
        <CodeInputField id_age="inputAgeStart" placeholder_age="Age(Start)" selectAge={addAgeStart} />
      </div>
      <div>
        <CodeInputField id_age="inputAgeEnd" placeholder_age="Age(End)" selectAge={addAgeEnd} />
      </div>
      <div>
        <CodeInputField id_gender="inputGender" placeholder_gender="Gender" selectGender={addGender} />
      </div>
      <div>
        <button type="button">Submit</button>
      </div>
    </div>
  );
}

export default RuleCreator;
