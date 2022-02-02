import { Component } from 'react';

const config = require("../config/config.json");

class Kafkas extends Component {
  constructor(props) {
    super(props);

    this.state = {
      kafkas: [],
      kafka: "",
      topics: []
    };
  }

  componentDidMount() {
    const kafkaNames = config["KAFKAS"].map(cluster => cluster["ENDPOINT"]);
    this.setState({
      kafkas: kafkaNames,
      kafka: kafkaNames[0]
    });
    
    // get the list of topics in the destination cluster
    // TODO: Move to utility (duplicate code with AddStreamForm)
    const firstKafka = config["KAFKAS"][0];
    const restProxyURL = `http://${firstKafka["REST_PROXY"]["HOST"]}:${firstKafka["REST_PROXY"]["PORT"]}`;
    const topicList = fetch(`${restProxyURL}/topics`)
                              .then(response => response.json())
                              .then(response => {
                                if (Array.isArray(response)) {
                                  this.setState({
                                    topics: response
                                  });
                                } else {
                                  throw Error("Failed to get topic list for dest cluster: " + response.message);
                                }
                              })
                              .catch(error => {
                                this.setState({
                                  error
                                });
                              });
  }

  // get a list of topics for a cluster via REST Proxy
  // TODO: Duplicate code with AddStreamForm.js (consolidate into utility)
  getTopicList() {
    // TODO: Better error handling in general in here
    const kafka = config["KAFKAS"].find((kafka) => { return kafka["ENDPOINT"] === this.state.kafka; });
    const kafkaRESTURL = `http://${kafka["REST_PROXY"]["HOST"]}:${kafka["REST_PROXY"]["PORT"]}`;

    fetch(`${kafkaRESTURL}/topics`)
      .then(response => response.json())
      .then(response => {
        this.setState({
          topics: response.sort(),
          sourceTopic: response[0]
        });
      })
      .catch(error => {
        this.setState({
          error
        });
      });
  }

  async handleChange(changeObject) {
    await this.setState(changeObject);
    this.getTopicList();
  }

  render() {
    return (
      <div>
        <h1 className="display-4">Kafkas</h1>

        <div className="form-group row">
          <div className="col-sm-6">
            <select className="form-control" id="clusterList" onChange={(e) => this.handleChange({ kafka: e.target.value })}>
              {this.state.kafkas && this.state.kafkas.map((kafka) => (
                <option key={kafka} value={kafka}>{kafka}</option>
              ))}
            </select>
          </div>
        </div>

        <table id="kafkaTopics" className="table table-sm">
          <thead>
            <tr>
              <th>Topic Name</th>
            </tr>
          </thead>
          <tbody>
            {this.state.topics && this.state.topics.sort().map((topic) => (
              <tr key={topic}>
                <td>{topic}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }
}

export default Kafkas;
