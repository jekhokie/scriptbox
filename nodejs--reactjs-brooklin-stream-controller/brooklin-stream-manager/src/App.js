import './App.css';
import { Routes, Route } from 'react-router-dom';
import HOCRouter from './HOCRouter';

import Streams from './components/Streams';
import AddStreamForm from './components/AddStreamForm';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route exact path="/" element={<HOCRouter Component={Streams} />} />
        <Route path="/addStream" element={<HOCRouter Component={AddStreamForm} />} />
      </Routes>
    </div>
  );
}

export default App;
