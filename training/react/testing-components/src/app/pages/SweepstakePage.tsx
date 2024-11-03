import { FormEvent, useState } from 'react';
import { useParticipantList } from '../state/hooks/useParticipantList';
import { useSweepstakeResult } from '../state/hooks/useSweepstakeResult';

import './Sweepstake.css';
import Card from '../components/Card';

const SweepstakePage = () => {
  const [participant, setParticipant] = useState('');
  const [secretFriend, setSecretFriend] = useState('');
  const participants = useParticipantList();
  const sweepstakeResult = useSweepstakeResult();

  const raffleOff = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const currentSecretFriend = sweepstakeResult.get(participant);
    if (currentSecretFriend) setSecretFriend(currentSecretFriend);
  };

  return (
    <Card>
      <section className="sweepstake">
        <form onSubmit={raffleOff}>
          <select
            required
            name="participant"
            id="participant"
            value={participant}
            onChange={(event) => setParticipant(event.target.value)}
          >
            <option>Select your name</option>
            {participants.map((participant) => (
              <option key={participant}>{participant}</option>
            ))}
          </select>
          <button type="submit" className="button-sorter">
            Raffle off
          </button>
        </form>
        {secretFriend && <p role="alert">{secretFriend}</p>}
        <footer className="sweeepstake">
          <img
            src="/assets/images/airplane.png"
            className="airplane"
            alt="An airplane drawn"
          />
        </footer>
      </section>
    </Card>
  );
};

export default SweepstakePage;
