import React from "react";
import ReactDOM from "react-dom";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import "./index.css";
import "typeface-roboto";
import App from "./Pages/App/App";
import Admin from "./Components/Admin/Admin";
import * as serviceWorker from "./Util/serviceWorker";
import Visualization from "./Components/Visualization/Visualization";

import { Provider } from "react-redux";
import { createStore, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";

import selectedCodesReducer from "./Store/Reducers/selected"; //TODO: change name to selectedCodesReducer

//enabling redux dev-tools
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(selectedCodesReducer, composeEnhancers(applyMiddleware(thunk)));

const notFound = () => <h1>Not Found</h1>;

const routing = (
  //TODO: get rid of Sandbox route used for testing
  <Provider store={store}>
    <BrowserRouter>
      <div>
        <Switch>
          <Route exact path="/" component={App} />
          <Route path="/admin" component={Admin} />
          <Route path="/visualization" component={Visualization} />
          <Route>{notFound}</Route>
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>
);

ReactDOM.render(routing, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
