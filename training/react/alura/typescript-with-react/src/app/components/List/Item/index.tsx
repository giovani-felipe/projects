import style from '../List.module.scss';

export default function Item(props: { name: string; time: string }) {
  return (
    <li className={style.item}>
      <h3>{props.name}</h3>
      <span>{props.time}</span>
    </li>
  );
}
