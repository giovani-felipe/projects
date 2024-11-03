import { useRecoilValue } from 'recoil';
import { errorState } from '../atom';

const useErrorMessage = () => {
  const message = useRecoilValue(errorState);
  return message;
};

export default useErrorMessage;
