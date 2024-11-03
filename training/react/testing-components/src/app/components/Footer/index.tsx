import { useNavigate } from 'react-router-dom';
import { useParticipantList } from '../../state/hooks/useParticipantList';
import './style.css';
import { useSweepstake } from '../../state/hooks/useSweepstake';

const FooterComponent = () => {
  const participants = useParticipantList();
  const navigate = useNavigate();
  const sweepstake = useSweepstake();

  const start = () => {
    sweepstake();
    navigate('/sweepstakes');
  };

  return (
    <footer className="footer-configurations">
      <button
        className="button"
        disabled={participants.length < 3}
        onClick={start}
      >
        Start joking
      </button>
      <img src="../../../assets/images/bags.png" alt="Shopping bags" />
    </footer>
  );
};

export default FooterComponent;
