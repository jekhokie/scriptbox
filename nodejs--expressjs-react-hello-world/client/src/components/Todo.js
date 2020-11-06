import React, { Component, Fragment } from 'react';

class Todo extends Component {
  render() {
    const todo = this.props.todo;

    return (
      <Fragment>
        <tr id="todo-{todo.id}">
          <td>{todo.id}</td>
          <td>{todo.text}</td>
          <td>{todo.done.toString()}</td>
        </tr>
      </Fragment>
    )
  }
}

export default Todo;
