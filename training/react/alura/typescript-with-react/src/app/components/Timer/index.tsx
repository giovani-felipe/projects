import Button from '../Button';
import style from './Timer.module.scss';
import Watch from './Watch';

export default function Timer() {
  return (
    <div className={style.timer}>
      <p className={style.title}>Select a card and starting the timer</p>
      <div className={style.watchWrapper}>
        <Watch />
      </div>
      <Button>Start!</Button>
    </div>
  );
}
