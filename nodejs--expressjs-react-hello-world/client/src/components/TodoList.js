import React, { Component, Fragment } from 'react';
import Todo from './Todo';

// configuration for API endpoint
const SERVER_API = process.env.SERVER_API || 'http://localhost:8000';

class TodoList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      error: null,
      isLoaded: false,
      todos: [],
    };
  }

  componentDidMount() {
    fetch(`${SERVER_API}/todos`)
    .then(res => res.json())
    .then(
      (result) => {
        console.log(result);
        this.setState({
          isLoaded: true,
          todos: result
        });
      },
      (error) => {
        this.setState({
          isLoaded: true,
          error
        });
      }
    )
  }

  render() {
    return (
      <Fragment>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Text</th>
              <th>Done</th>
            </tr>
          </thead>
          <tbody>
            {this.state.todos.map(todo => <Todo key={todo.id} todo={todo} />)}
          </tbody>
        </table>
      </Fragment>
    )
  }
}

export default TodoList;
