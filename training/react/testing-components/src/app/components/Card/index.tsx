import { ReactNode } from 'react';
import './style.scss';

const Card = ({ children }: { children: ReactNode }) => {
  return <div className="card">{children}</div>;
};

export default Card;
