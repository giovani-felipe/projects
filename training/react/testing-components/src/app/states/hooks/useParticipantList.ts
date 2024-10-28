import { useRecoilValue } from 'recoil';
import { participantListState } from '../atom';

export const useParticipantList = () => {
  return useRecoilValue(participantListState);
};
