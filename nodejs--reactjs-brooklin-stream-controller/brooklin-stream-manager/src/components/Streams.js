import { Component } from 'react';
import { Link } from "react-router-dom";

const config = require("../config/config.json");
const brooklinURL = `http://${config["BROOKLIN"]["HOST"]}:${config["BROOKLIN"]["PORT"]}`;

class Streams extends Component {
  constructor(props) {
    super(props);

    this.state = {
      streams: [],
    };

    this.delete = this.delete.bind(this);
    this.pause = this.pause.bind(this);
    this.resume = this.resume.bind(this);
  }

  componentDidMount() {
    fetch(`${brooklinURL}/datastream/`)
      .then(response => response.json())
      .then(response => {
        // this needs to be updated to accommodate pagination
        this.setState({
          streams: response.elements
        });
      })
      .catch(error => {
        this.setState({
          error
        });
      });
  }

  delete(streamName) {
    fetch(`${brooklinURL}/datastream/${streamName}`, {
      method: "DELETE",
    })
      .then(response => {
        if (response.ok) {
          console.log("SUCCESS");

          // re-calculate the stream list
          const newStreamList = this.state.streams.filter((stream) => stream.name !== streamName)
          this.setState({
            streams: newStreamList
          });
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

  resume(streamName) {
    fetch(`${brooklinURL}/datastream/${streamName}?action=resume`, {
      method: "POST",
    })
      .then(response => {
        if (response.ok) {
          console.log("SUCCESS");

          // re-calculate the stream list
          this.setState({
            streams: this.state.streams.map(stream => {
              if (stream.name === streamName) {
                return { ...stream, Status: "READY" };
              }
              return stream;
            })
          })
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

  pause(streamName) {
    fetch(`${brooklinURL}/datastream/${streamName}?action=pause`, {
      method: "POST",
    })
      .then(response => {
        if (response.ok) {
          console.log("SUCCESS");

          // re-calculate the stream list
          this.setState({
            streams: this.state.streams.map(stream => {
              if (stream.name === streamName) {
                return { ...stream, Status: "PAUSED" };
              }
              return stream;
            })
          })
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

  render() {
    return (
      <div>
        <h1 className="display-4">Configured BMM Streams</h1>
        <table id="brooklinStreams" className="table table-sm">
          <thead>
            <tr>
              <th>Stream Name</th>
              <th>Topic Name</th>
              <th>Source</th>
              <th>Source Partitions</th>
              <th>Destination</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {this.state.streams && this.state.streams.map((stream) => (
              <tr key={stream.name}>
                <td>{stream.name}</td>
                <td>{stream.source.connectionString.split("/").pop()}</td>
                <td>{stream.source.connectionString.split("/")[2]}</td>
                <td>{stream.source.partitions}</td>
                <td>{stream.destination.connectionString.split("/")[2]}</td>
                <td>{stream.Status}</td>
                <td>
                  <button disabled={stream.Status === "READY" || stream.Status == "INITIALIZING" ? true : ""} type="button" className="btn pt-0" onClick={(e) => this.resume(stream.name)}>
                    <i className="fa fa-play text-success" aria-hidden="true"></i>
                  </button>
                  <button disabled={stream.Status !== "READY" || stream.Status == "INITIALIZING" ? true : ""} type="button" className="btn pt-0" onClick={(e) => this.pause(stream.name)}>
                    <i className="fa fa-pause text-warning" aria-hidden="true"></i>
                  </button>
                  <button type="button" className="btn pt-0" onClick={(e) => this.delete(stream.name)}>
                    <i className="fa fa-trash text-danger" aria-hidden="true"></i>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <Link to="/addStream">
          <button className="btn btn-success" type='button'>Add Stream</button>
        </Link>
      </div>
    )
  }
}

export default Streams;
