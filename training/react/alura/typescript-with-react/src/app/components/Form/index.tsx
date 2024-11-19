import { Dispatch, FormEvent, SetStateAction, useState } from 'react';
import { Task } from '../../types/task';
import ButtonComponent from '../Button';
import style from './Form.module.scss';

export default function Form({
  setTasks,
}: {
  setTasks: Dispatch<SetStateAction<Task[]>>;
}) {
  const [task, setTask] = useState('');
  const [time, setTime] = useState('00:00:01');

  function addTask(event: FormEvent) {
    event.preventDefault();
    setTasks((tasks) => [
      ...tasks,
      {
        name: task,
        time: time,
        selected: false,
        completed: false,
        id: new Date().getTime(),
      },
    ]);
    setTask('');
    setTime('00:00');
  }

  return (
    <form className={style.Form} onSubmit={addTask}>
      <div className={style.inputContainer}>
        <label htmlFor="task">Add a new subject</label>
        <input
          type="text"
          name="name"
          value={task}
          onChange={(event) => setTask(event.target.value)}
          id="task"
          placeholder="What do you want to study?"
          required
        />
      </div>
      <div className={style.inputContainer}>
        <label htmlFor="time">Time</label>
        <input
          type="time"
          step="1"
          name="time"
          value={time}
          onChange={(event) => setTime(event.target.value)}
          id="time"
          min="00:00:00"
          max="01:30:00"
          required
        />
      </div>
      <ButtonComponent type="submit">Add</ButtonComponent>
    </form>
  );
}
