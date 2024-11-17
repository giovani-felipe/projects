import { useSetRecoilState } from 'recoil';
import { secretFriendState } from '../atom';
import { raffleOff } from '../helpers/raffleOff';
import { useParticipantList } from './useParticipantList';

export const useSweepstake = () => {
  const participants = useParticipantList();
  const setSecretFriend = useSetRecoilState(secretFriendState);

  return () => {
    const result = raffleOff(participants);
    setSecretFriend(result);
  };
};
