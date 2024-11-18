import Form from '../components/Form';
import List from '../components/List';
import Timer from '../components/Timer';
import style from './app.module.scss';

export function App() {
  return (
    <div className={style.App}>
      <Form />
      <List />
      <Timer />
    </div>
  );
}

export default App;
