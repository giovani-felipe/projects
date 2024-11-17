import { useRecoilValue } from 'recoil';
import { secretFriendState } from '../atom';

export const useSweepstakeResult = () => {
  return useRecoilValue(secretFriendState);
};
