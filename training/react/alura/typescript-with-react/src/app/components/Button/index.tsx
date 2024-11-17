import { Component } from 'react';
import style from './Button.module.scss';

class Button extends Component {
  render() {
    return <button className={style.button}>Button</button>;
  }
}

export default Button;
