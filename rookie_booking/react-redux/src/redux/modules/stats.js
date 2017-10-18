
// ///////////////////////////////////////////////////////////////////////////////////
// //////////////////////////////// Constants ////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////////////

const FETCHING_RESULTS         = 'FETCHING_RESULTS';
const FETCHING_RESULTS_SUCCESS = 'FETCHING_RESULTS_SUCCESS';
const FETCHING_RESULTS_FAILURE = 'FETCHING_RESULTS_FAILURE';
const STATS_SAGA               = 'STATS_SAGA';

// ///////////////////////////////////////////////////////////////////////////////////
// ///////////////////////////// Action Creators /////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////////////

export function getResultsFromSaga() {
    return {
        type: STATS_SAGA
    };
}

export function getData() {
    return {
        type: FETCHING_RESULTS
    };
}

export function getDataSuccess(data) {
    return {
        type: FETCHING_RESULTS_SUCCESS,
        data
    };
}

export function getDataFailure() {
    return {
        type: FETCHING_RESULTS_FAILURE
    };
}

// ///////////////////////////////////////////////////////////////////////////////////
// //////////////////////////////// Reducers /////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////////////

const initialState = {
    currentUser: "",
    // currentUserWins:  0,
    // currentUserLoses: 0,
    data       : {},
    dataFetched: false,
    isFetching : false,
    error      : false
};

export default function statsReducer(state = initialState, action) {
    switch (action.type) {
    case FETCHING_RESULTS:
        return {
            ...state,
            data      : {},
            isFetching: true,
            error     : false
        };
    case FETCHING_RESULTS_SUCCESS:
        return {
            ...state,
            data       : action.response_data.data,
            currentUser: action.response_data.currentUser,
            isFetching : false,
            error      : false,
            dataFetched: true
        };
    case FETCHING_RESULTS_FAILURE:
        return {
            ...state,
            isFetching: false,
            error     : true
        };
    default:
        return state;
    }
}

// ///////////////////////////////////////////////////////////////////////////////////
// /////////////////////////////// Selectors /////////////////////////////////////////
// ///////////////////////////////////////////////////////////////////////////////////

export function selectorUserGames(state) {
    console.log('selectorUserGames(state)')
    // return Object.entries(state.results.data).reduce(function (sum, [keyName, value]) {
    //     return state.results.currentUser === value.winner ? sum + 1 : sum
    // }, 0)
}

export function selectorUserWins(state) {
    console.log('selectorUserWins(state)')
    // return Object.entries(state.results.data).reduce(function (sum, [keyName, value]) {
    //     return state.results.currentUser === value.winner ? sum + 1 : sum
    // }, 0)
}

export function selectorUserLosses(state) {
    console.log('selectorUserLosses(state)')
    // return Object.entries(state.results.data).reduce(function (sum, [keyName, value]) {
    //     return state.results.currentUser === value.winner ? sum + 1 : sum
    // }, 0)
}



export function selectorUserWinsCount(state) {
    console.log('selectorUserWinsCount(state)')
    return Object.entries(state.results.data).reduce(function (sum, [keyName, value]) {
        return state.results.currentUser === value.winner ? sum + 1 : sum
    }, 0)
}

export function selectorUserLossesCount(state) {
    console.log('selectorUserLossesCount(state)')
    return Object.entries(state.results.data).reduce(function (sum, [keyName, value]) {
        return state.results.currentUser === value.loser ? sum + 1 : sum
    }, 0)
}
