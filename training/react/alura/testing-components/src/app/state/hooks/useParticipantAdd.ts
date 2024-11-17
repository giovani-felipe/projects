import { useRecoilState, useSetRecoilState } from 'recoil';
import { errorState, participantListState } from '../atom';

export const useParticipantAdd = () => {
  const setList = useSetRecoilState(participantListState);
  const [list] = useRecoilState(participantListState);
  const setErrorMessage = useSetRecoilState(errorState);
  return (name: string) => {
    if (list.includes(name)) {
      setErrorMessage('Duplicate names are not allowed');
      setTimeout(() => {
        setErrorMessage('');
      }, 5000);
      return;
    }

    return setList((state) => [...state, name]);
  };
};
