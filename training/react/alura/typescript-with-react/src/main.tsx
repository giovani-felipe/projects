import { StrictMode } from 'react';
import * as ReactDOM from 'react-dom/client';
import App from './app/pages/app';
import './styles.scss';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement,
);

process.env.NODE_ENV === 'development'
  ? root.render(
      <StrictMode>
        <App />
      </StrictMode>,
    )
  : root.render(<App />);
