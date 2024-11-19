import { Component, ReactNode } from 'react';
import style from './Button.module.scss';

type ButtonProps = {
  type?: 'button' | 'submit' | 'reset';
  children: ReactNode;
  onClick?: () => void;
};

function Button({ type = 'button', onClick, children }: ButtonProps) {
  return (
    <button type={type} className={style.button} onClick={onClick}>
      {children}
    </button>
  );
}

class ButtonComponent extends Component<{
  type?: 'button' | 'submit' | 'reset';
  children: ReactNode;
  onClick?: () => void;
}> {
  render() {
    const { type = 'button', onClick } = this.props;
    return (
      <Button type={type} onClick={onClick}>
        {this.props.children}
      </Button>
    );
  }
}

export default ButtonComponent;
