import React     from 'react';
import PropTypes from 'prop-types';
import { Table } from "react-bootstrap"


const IndividualSummary = (props) => {
    return (
        <div>
            <div>IndividualSummary</div>
            <Table  bordered condensed hover>
                <thead>
                    <tr>
                        <td>key</td>

                        <td>id</td>
                        <td>winner</td>
                        <td>loser</td>
                        <td>elo</td>
                        <td>balls#</td>
                        <td>date</td>
                    </tr>
                </thead>
                <tbody>
                    {/*{*/}
                        {/*Object.keys(props.results).map((keyName, keyIndex) =>*/}
                            {/*<tr key={props.results[keyName].id}>*/}
                                {/*<td>{props.results[keyName].id}</td>*/}
                                {/*<td>{props.results[keyName].winner}</td>*/}
                                {/*<td>{props.results[keyName].loser}</td>*/}
                                {/*<td>{props.results[keyName].elo}</td>*/}
                                {/*<td>{props.results[keyName].balls_left}</td>*/}
                                {/*<td>{props.results[keyName].date}</td>*/}
                            {/*</tr>*/}
                        {/*)*/}
                    {/*}*/}
                    {
                        Object.entries(props.results).map(([keyName, value]) =>
                            <tr key={value.id}>
                                <td>{keyName}</td>
                                <td>{value.id}</td>
                                <td>{value.winner}</td>
                                <td>{value.loser}</td>
                                <td>{value.elo}</td>
                                <td>{value.balls_left}</td>
                                <td>{value.date}</td>
                            </tr>
                        )
                    }
                </tbody>
            </Table>
        </div>
    );
};

IndividualSummary.propTypes    = {
    results: PropTypes.object.isRequired
};
IndividualSummary.defaultProps = {};

export default IndividualSummary;
