import Form from '../components/Form';
import List from '../components/List';
import style from './app.module.scss';

export function App() {
  return (
    <div className={style.App}>
      <Form />
      <List />
    </div>
  );
}

export default App;
