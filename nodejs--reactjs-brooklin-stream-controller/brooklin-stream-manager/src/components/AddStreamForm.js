import { Component } from 'react';

// TODO: consolidate into single file of vars
const config = require("../config/config.json");

class AddStreamForm extends Component {
  constructor(props) {
    super(props);
    const clusterList = config["KAFKAS"].map(cluster => cluster["ENDPOINT"]).sort();
    const topicDefaults = config["TOPIC_DEFAULTS"];

    this.state = {
      topics: [],
      sourceTopic: "",
      sourceClusters: clusterList,
      sourceCluster: clusterList[0],
      destClusters: clusterList,
      destCluster: clusterList[0],
      partitions: topicDefaults["PARTITIONS"],
      replicationFactor: topicDefaults["REPLICATION_FACTOR"],
      error: "",
    };

    this.handleChange = this.handleChange.bind(this);
    this.create = this.create.bind(this);
    this.cancel = this.cancel.bind(this);
  }

  // get a list of topics for a cluster via REST Proxy
  getTopicList() {
    // TODO: Better error handling in general in here
    const kafka = config["KAFKAS"].find((kafka) => {
                    return kafka["ENDPOINT"] === this.state.sourceCluster;
                  });
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

  componentDidMount() {
    this.getTopicList();
  }

  async create(e) {
    e.preventDefault();

    const sourceKafka = config["KAFKAS"].find((kafka) => { return kafka["ENDPOINT"] === this.state.sourceCluster; });
    const destKafka = config["KAFKAS"].find((kafka) => { return kafka["ENDPOINT"] === this.state.destCluster; });
    const sourceKafkaRESTURL = `http://${sourceKafka["REST_PROXY"]["HOST"]}:${sourceKafka["REST_PROXY"]["PORT"]}`;
    const destKafkaRESTURL = `http://${destKafka["REST_PROXY"]["HOST"]}:${destKafka["REST_PROXY"]["PORT"]}`;

    // check that the topic exists in the destination cluster, create if necessary
    // get the cluster ID
    // no need to paginate because the REST proxy is assumed 1:1 with destination cluster
    const clusterId = await fetch(`${destKafkaRESTURL}/v3/clusters`)
                              .then(response => response.json())
                              .then(response => {
                                if (response.data) {
                                  return response.data[0].cluster_id;
                                } else {
                                  throw Error("Failed to get clusters for clusterId: " + response.message);
                                }
                              })
                              .catch(error => {
                                this.setState({
                                  error
                                });
                              });

    // get the list of topics in the destination cluster
    // TODO: Will likely need to paginate
    const topicList = await fetch(`${destKafkaRESTURL}/topics`)
                              .then(response => response.json())
                              .then(response => {
                                if (Array.isArray(response)) {
                                  return response;
                                } else {
                                  throw Error("Failed to get topic list for dest cluster: " + response.message);
                                }
                              })
                              .catch(error => {
                                this.setState({
                                  error
                                });
                              });

    // create the topic in the destination cluster if it does not yet exist
    // TODO: Figure out if it's better to fail if the topic already exists (name collisions)
    if (!topicList.includes(this.state.sourceTopic)) {
      await fetch(`${destKafkaRESTURL}/v3/clusters/${clusterId}/topics`, {
              method: "POST",
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                "topic_name": this.state.sourceTopic,
                "partitions_count": this.state.partitions,
                "replication_factor": this.state.replicationFactor,
              })
            })
              .then(response => {
                console.log(response);
                if (response.ok) {
                  console.log("Created topic in target cluster");
                } else {
                  throw Error(response.message);
                }
              })
              .catch(error => {
                this.setState({
                  error
                });
              });
    }

    // create the data stream (Mirroring) in Brooklin
    const streamName = this.state.sourceCluster + "-" + this.state.sourceTopic + "-" + this.state.destCluster;
    const sourceConnString = `kafka://${sourceKafka["ENDPOINT"]}:${sourceKafka["INTERNAL_PORT"]}/${this.state.sourceTopic}`;
    const brooklinURL = `http://${config["BROOKLIN"]["HOST"]}:${config["BROOKLIN"]["PORT"]}`;

    await fetch(`${brooklinURL}/datastream/`, {
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
          this.props.navigate("/");
        } else {
          return response.json()
            .then(response => {
              throw Error(response.message);
            });
        }
      })
      .catch(error => {
        this.setState({
          error
        });
      });
  }

  cancel(e) {
    e.preventDefault();
    this.props.navigate("/");
  }

  async handleChange(changeObject) {
    await this.setState(changeObject);
    this.getTopicList();
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

          <div className="form-group row">
            <label htmlFor="destPartitions" className="col-sm-2 col-form-label">Destination Partitions</label>
            <div className="col-sm-6">
              <input type="text" className="form-control" id="destPartitions" value={this.state.partitions} onChange={(e) => this.handleChange({ partitions: e.target.value })} />
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
