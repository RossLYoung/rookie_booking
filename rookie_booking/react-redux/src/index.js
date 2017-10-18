import React, { Component } from 'react';
import ReactDOM             from 'react-dom';
import { Provider }         from 'react-redux';
import createSagaMiddleware from 'redux-saga';
import { Grid }             from 'react-bootstrap'
import { createStore, applyMiddleware, compose, combineReducers } from 'redux';

import { StatsContainer } from './containers';
import { statsSaga }      from 'redux/sagas'
import * as reducers        from 'redux/modules'

const sagaMiddleware = createSagaMiddleware()

/*eslint-disable */
const composeSetup = process.env.NODE_ENV !== 'production' && typeof window === 'object' &&
window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ?
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ : compose
/*eslint-enable */

const store = createStore(
    combineReducers(reducers),
    composeSetup(applyMiddleware(sagaMiddleware)), // allows redux devtools to watch sagas
);

sagaMiddleware.run(statsSaga);

ReactDOM.render(
    <Provider store={store}>
        <div>
            <StatsContainer />
        </div>
    </Provider>,

    document.getElementById('app')
);
