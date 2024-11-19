import style from './Watch.module.scss';

type WatchProps = {
  time?: number;
};

export default function Watch({ time = 0 }: WatchProps) {
  const minutes = Math.floor(time / 60) % 60;
  const seconds = time % 60;

  const [minuteTens, minuteUnit] = minutes.toString().padStart(2, '0');
  const [secondTens, secondUnit] = seconds.toString().padStart(2, '0');

  return (
    <>
      <span className={style.watchNumber}>{minuteTens}</span>
      <span className={style.watchNumber}>{minuteUnit}</span>
      <span className={style.watchSplit}>:</span>
      <span className={style.watchNumber}>{secondTens}</span>
      <span className={style.watchNumber}>{secondUnit}</span>
    </>
  );
}
