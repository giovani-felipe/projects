import { Component } from 'react';
import Button from '../Button';
import style from './Form.module.scss';

class Form extends Component {
  render() {
    return (
      <form className={style.Form}>
        <div className={style.inputContainer}>
          <label htmlFor="task">Add a new subject</label>
          <input
            type="text"
            name="task"
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
            id="time"
            min="00:00:00"
            max="01:30:00"
            required
          />
        </div>
        <Button>Add</Button>
      </form>
    );
  }
}

export default Form;
