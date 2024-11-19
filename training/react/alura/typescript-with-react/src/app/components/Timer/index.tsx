import ButtonComponent from '../Button';
import style from './Timer.module.scss';
import Watch from './Watch';
import { Task } from '../../types/task';
import { useEffect, useState } from 'react';
import { hourToSeconds as timeToSeconds } from '../../common/date';

type TimerProps = {
  selectedTask?: Task;
  finishTask: () => void;
};

export default function Timer({ selectedTask, finishTask }: TimerProps) {
  const [time, setTime] = useState<number>(0);

  useEffect(() => {
    if (selectedTask?.time) setTime(timeToSeconds(selectedTask.time));
  }, [selectedTask]);

  function regressive(counter = 0) {
    setTimeout(() => {
      if (counter === 0) {
        finishTask();
        return;
      }
      setTime(counter - 1);
      regressive(counter - 1);
    }, 1000);
  }

  return (
    <div className={style.timer}>
      <p className={style.title}>Select a card and starting the timer</p>
      <div className={style.watchWrapper}>
        <Watch time={time} />
      </div>
      <ButtonComponent onClick={() => regressive(time)}>Start!</ButtonComponent>
    </div>
  );
}
