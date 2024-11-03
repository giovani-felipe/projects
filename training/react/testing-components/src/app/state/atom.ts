import { atom } from 'recoil';

export const participantListState = atom<string[]>({
  key: 'participantState',
  default: [],
});

export const secretFriendState = atom<Map<string, string>>({
  key: 'secretFriendState',
  default: new Map(),
});

export const errorState = atom<string>({
  key: 'errorState',
  default: '',
});
