export function hourToSeconds(time: string) {
  const [hora = 0, minutes = 0, seconds = 0] = time.split(':').map(Number);
  return hora * 3600 + minutes * 60 + seconds;
}
