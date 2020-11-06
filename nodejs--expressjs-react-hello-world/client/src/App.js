import React, { Fragment } from 'react';

// component imports
import AppHeader from './components/AppHeader';
import TodoList from './components/TodoList';

const App = ({ classes }) => (
  <Fragment>
    <AppHeader />
    <main>
      <TodoList />
    </main>
  </Fragment>
);

export default App;
