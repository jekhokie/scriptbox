import './App.css';
import { Routes, Route } from 'react-router-dom';
import HOCRouter from './HOCRouter';

import Streams from './components/Streams';
import Kafkas from './components/Kafkas';
import AddStreamForm from './components/AddStreamForm';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route exact path="/" element={<HOCRouter Component={Streams} />} />
        <Route path="/kafkas" element={<HOCRouter Component={Kafkas} />} />
        <Route path="/addStream" element={<HOCRouter Component={AddStreamForm} />} />
      </Routes>
    </div>
  );
}

export default App;
