import { Task } from '../../types/task';
import Item from './Item';
import style from './List.module.scss';

type ListProps = {
  tasks: Task[];
  selectTask: (task: Task) => void;
};

function List({ tasks, selectTask }: ListProps) {
  return (
    <aside className={style.List}>
      <h2>Studies of the day</h2>
      <ul>
        {tasks.map((task) => (
          <Item key={task.id} task={task} selectTask={selectTask} />
        ))}
      </ul>
    </aside>
  );
}

export default List;
