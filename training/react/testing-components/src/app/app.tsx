// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './app.css';
import { RecoilRoot } from 'recoil';
import ConfigurationPage from './pages/ConfigurationPage';
import SweepstakePage from './pages/SweepstakePage';

export function App() {
  return (
    <BrowserRouter>
      <RecoilRoot>
        <Routes>
          <Route path="/" Component={ConfigurationPage} />
          <Route path="/sweepstakes" Component={SweepstakePage} />
        </Routes>
      </RecoilRoot>
    </BrowserRouter>
  );
}

export default App;
