import { atom } from 'recoil';

export const participantListState = atom<string[]>({
  key: 'participantState',
  default: [],
});

export const errorState = atom<string>({
  key: 'errorState',
  default: '',
});
