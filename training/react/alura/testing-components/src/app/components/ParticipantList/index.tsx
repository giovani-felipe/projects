import { useParticipantList } from '../../state/hooks/useParticipantList';

const ParticipantListComponent = () => {
  const participants = useParticipantList();

  return (
    <ul>
      {participants.map((participant) => (
        <li key={participant}>{participant}</li>
      ))}
    </ul>
  );
};

export default ParticipantListComponent;
