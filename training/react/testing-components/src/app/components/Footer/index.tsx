import { useNavigate } from 'react-router-dom';
import { useParticipantList } from '../../states/hooks/useParticipantList';
import './style.scss';

const FooterComponent = () => {
  const participants = useParticipantList();
  const navigate = useNavigate();

  const start = () => navigate('/sweepstakes');

  return (
    <footer className="footer-configurations">
      <button
        className="button"
        disabled={participants.length < 3}
        onClick={start}
      >
        Start joking
      </button>
      <img src="/assets/images/bags.png" alt="Shopping bags" />
    </footer>
  );
};

export default FooterComponent;
