import style from './Watch.module.scss';

export default function Watch() {
  return (
    <>
      <span className={style.watchNumber}>0</span>
      <span className={style.watchNumber}>0</span>
      <span className={style.watchSplit}>:</span>
      <span className={style.watchSplit}>0</span>
      <span className={style.watchSplit}>0</span>
    </>
  );
}
