import { Task } from '../../../types/task';
import style from './Item.module.scss';

type ItemProps = {
  task: Task;
  selectTask: (task: Task) => void;
};

export default function Item({ task, selectTask }: ItemProps) {
  return (
    <li
      className={`${style.item} ${task.selected ? style.itemSelected : ''} ${task.completed ? style.itemCompleted : ''}`}
      onClick={() => !task.completed && selectTask(task)}
    >
      <h3>{task.name}</h3>
      <span>{task.time}</span>
      {task.completed && <span className={style.completed}></span>}
    </li>
  );
}
