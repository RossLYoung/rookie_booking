import React, { Component }   from 'react';
import PropTypes              from 'prop-types';
import { connect }            from 'react-redux';
import { bindActionCreators } from 'redux';

import { Row, Col }          from 'react-bootstrap';
import { IndividualSummary } from 'components';
import * as statsActions     from '../redux/modules/stats';
import {
    selectorUserGames,
    selectorUserWins,
    selectorUserLosses,
    selectorUserWinsCount,
    selectorUserLossesCount
} from '../redux/modules/stats';


class StatsContainer extends Component {

    componentDidMount() {
        if (!this.props.dataFetched) {
            this.props.getResultsFromSaga()
        }
    }

    render() {
        return (
            <Col xs={12}>
                <h2>Wincount {this.props.winCount}</h2>
                <h2>Loscount {this.props.lossesCount}</h2>

                <IndividualSummary results={this.props.results} />
            </Col>
        );
    }
}


StatsContainer.propTypes    = {
    isFetching        : PropTypes.bool.isRequired,
    dataFetched       : PropTypes.bool.isRequired,
    results           : PropTypes.object.isRequired,

    getResultsFromSaga: PropTypes.func.isRequired
};
StatsContainer.defaultProps = {};


function mapStateToProps(state) {
    return {
        isFetching : state.results.isFetching,
        dataFetched: state.results.dataFetched,
        results    : state.results.data,

        games      : selectorUserGames(state),
        wins       : selectorUserWins(state),
        lossesCount: selectorUserLosses(state),
        winCount   : selectorUserWinsCount(state),
        lossesCount: selectorUserLossesCount(state)
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators(statsActions, dispatch);
}
export default connect(mapStateToProps, mapDispatchToProps)(StatsContainer);

