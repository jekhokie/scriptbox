import { Component } from 'react';

// TODO: consolidate into single file of vars
const config = require("../config/config.json");
const kafka1RESTURL = `http://${config["KAFKA_1_REST_PROXY"]["HOST"]}:${config["KAFKA_1_REST_PROXY"]["PORT"]}`
const brooklinURL = `http://${config["BROOKLIN"]["HOST"]}:${config["BROOKLIN"]["PORT"]}`;
const kafka1URI = `kafka://${config["KAFKA_1"]["HOST"]}:${config["KAFKA_1"]["INTERNAL_PORT"]}`

class AddStreamForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      topics: [],
      sourceTopic: "",
      sourceClusters: ["kafka1"],
      sourceCluster: "kafka1",
      destClusters: ["kafka2"],
      destCluster: "kafka2",
    };

    this.handleChange = this.handleChange.bind(this);
    this.create = this.create.bind(this);
    this.cancel = this.cancel.bind(this);
  }

  componentDidMount() {
    fetch(`${kafka1RESTURL}/topics`)
      .then(response => response.json())
      .then(response => {
        this.setState({
          topics: response,
          sourceTopic: response[0]
        });
      })
      .catch(error => {
        this.setState({
          error
        });
      });
  }

  handleChange(changeObject) {
    this.setState(changeObject)
  }

  create(e) {
    e.preventDefault();
    const streamName = this.state.sourceCluster + "-" + this.state.sourceTopic + "-" + this.state.destCluster;
    const sourceConnString = `${kafka1URI}/${this.state.sourceTopic}`;

    fetch(`${brooklinURL}/datastream/`, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "name": streamName,
        "connectorName": "kafkaMirroringConnector",
        "transportProviderName": "kafkaTransportProvider",
        "source": {
          "connectionString": sourceConnString,
          "partitions": 1
        },
        "metadata": {
          "owner": "test-user",
          "system.reuseExistingDestination": "false"
        }
      })
    })
      .then(response => {
        if (response.ok) {
          console.log("SUCCESS");
          this.props.navigate("/");
        } else {
          return response.json()
            .then(response => {
              throw Error(response.message);
            });
        }
      })
      .catch(error => {
        console.log("ERROR: " + error);
      });
  }

  cancel(e) {
    e.preventDefault();
    this.props.navigate("/");
  }

  render() {
    return (
      <div>
        <h1 className="display-4">Add BMM Stream</h1>

        <p>
          <b>NOTE:</b> In an ideal world, source clusters would be selectable and populate the source topic selector
          based on what topics were available, and the destination cluster would also be selectable. However, since this is a
          demo with only one source/destination cluster, the flow is a bit strange/unrealistic.
        </p>

        <form>
          <div className="form-group row">
            <label htmlFor="sourceCluster" className="col-sm-2 col-form-label">Source Cluster</label>
            <div className="col-sm-6">
              <select className="form-control" id="sourceCluster" onChange={(e) => this.handleChange({ sourceCluster: e.target.value })}>
                {this.state.sourceClusters && this.state.sourceClusters.map((sourceCluster) => (
                  <option key={sourceCluster} value={sourceCluster}>{sourceCluster}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="sourceTopic" className="col-sm-2 col-form-label">Source Topic</label>
            <div className="col-sm-6">
              <select className="form-control" id="sourceTopic" onChange={(e) => this.handleChange({ sourceTopic: e.target.value })}>
                {this.state.topics && this.state.topics.map((topic) => (
                  <option key={topic} value={topic}>{topic}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="destCluster" className="col-sm-2 col-form-label">Destination Cluster</label>
            <div className="col-sm-6">
              <select className="form-control" id="destCluster" onChange={(e) => this.handleChange({ destCluster: e.target.value })}>
                {this.state.destClusters && this.state.destClusters.map((destCluster) => (
                  <option key={destCluster} value={destCluster}>{destCluster}</option>
                ))}
              </select>
            </div>
          </div>

          <button className="btn btn-success mr-2" type='button' onClick={(e) => this.create(e)}>Create</button>
          <button className="btn btn-danger" type='button' onClick={(e) => this.cancel(e)}>Cancel</button>
        </form>
      </div>
    )
  }
}

export default AddStreamForm;
