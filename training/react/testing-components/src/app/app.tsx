// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import styles from './app.module.scss';
import { RecoilRoot } from 'recoil';
import ConfigurationPage from './pages/ConfigurationPage';

export function App() {
  return (
    <BrowserRouter>
      <RecoilRoot>
        <Routes>
          <Route path="/" Component={ConfigurationPage} />
        </Routes>
      </RecoilRoot>
    </BrowserRouter>
  );
}

export default App;
