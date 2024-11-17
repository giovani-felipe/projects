import style from './List.module.scss';

function Task(task: { name: string; time: string }) {
  return (
    <li key={task.name} className={style.item}>
      <h3>{task.name}</h3>
      <span>{task.time}</span>
    </li>
  );
}

function List() {
  const tasks = [
    {
      name: 'React',
      time: '02:00:00',
    },
    {
      name: 'Java Script',
      time: '01:00:00',
    },
  ];

  return (
    <aside className={style.List}>
      <h2>Studies of the day</h2>
      <ul>
        {tasks.map((task) => (
          <Task name={task.name} time={task.time} />
        ))}
      </ul>
    </aside>
  );
}

export default List;
