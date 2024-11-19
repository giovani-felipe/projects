import { useState } from 'react';
import FormComponent from '../components/Form';
import List from '../components/List';
import Timer from '../components/Timer';
import style from './app.module.scss';
import { Task } from '../types/task';

export function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task>();

  function handleTaskSelection(task: Task) {
    setSelectedTask(task);
    setTasks((tasks) =>
      tasks.map((item) => ({ ...item, selected: item.id === task.id })),
    );
  }

  function finishTask() {
    setTasks((tasks) =>
      tasks.map((item) => ({
        ...item,
        completed: item.id === selectedTask?.id ? true : item.completed,
      })),
    );
    setSelectedTask(undefined);
  }

  return (
    <div className={style.App}>
      <FormComponent setTasks={setTasks} />
      <List tasks={tasks} selectTask={handleTaskSelection} />
      <Timer selectedTask={selectedTask} finishTask={finishTask} />
    </div>
  );
}

export default App;
