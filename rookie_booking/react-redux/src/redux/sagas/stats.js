import { delay } from 'redux-saga';
import { put, takeEvery, all, fork, call } from 'redux-saga/effects';
import "regenerator-runtime/runtime";

import { endPoints, fetchAllResults } from 'api'


function* callFetchAllResults() {
    // console.log('getting groups');
    try {
        yield put({ type: 'FETCHING_RESULTS' });
        yield call(delay, 2000);
        const response_data = yield call(fetchAllResults, endPoints.ALL_POOL_RESULTS);

        // debugger
        // console.log(response);

        yield put({ type: 'FETCHING_RESULTS_SUCCESS', response_data: response_data });
    } catch (e) {
        console.log(e);
        yield put({
            type : 'FETCHING_RESULTS_FAILURE',
            error: true
        })
    }
}

function* getAllResultsSaga() {
    yield takeEvery('STATS_SAGA', callFetchAllResults);
}

export default function* statsSaga() {
    yield all([
        fork(getAllResultsSaga)
    ])
}
