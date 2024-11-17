import '@testing-library/jest-dom';
import { fireEvent, render } from '@testing-library/react';
import { RecoilRoot } from 'recoil';
import { useParticipantList } from '../state/hooks/useParticipantList';
import { useSweepstakeResult } from '../state/hooks/useSweepstakeResult';
import Sweepstake from './SweepstakePage';

vi.mock('../state/hooks/useParticipantList', () => {
  return { useParticipantList: vi.fn() };
});

vi.mock('../state/hooks/useSweepstakeResult', () => {
  return { useSweepstakeResult: vi.fn() };
});

describe('SweepstakePage', () => {
  const participants = ['Giovani', 'Felipe', 'Miguel'];
  const result = new Map([
    ['Giovani', 'Felipe'],
    ['Felipe', 'Miguel'],
    ['Miguel', 'Giovani'],
  ]);
  beforeEach(() => {
    vi.mocked(useParticipantList).mockReturnValue(participants);
    vi.mocked(useSweepstakeResult).mockReturnValue(result);
  });

  it('all participants can show their secret friend', () => {
    const { queryAllByRole } = render(
      <RecoilRoot>
        <Sweepstake />
      </RecoilRoot>
    );
    const options = queryAllByRole('option');
    expect(options).toHaveLength(participants.length + 1);
  });

  it('the secret friend is displayed when required', () => {
    const { getByRole } = render(
      <RecoilRoot>
        <Sweepstake />
      </RecoilRoot>
    );

    const select = getByRole('combobox');

    fireEvent.change(select, {
      target: { value: participants[0] },
    });

    const button = getByRole('button');
    fireEvent.click(button);

    const secretFriend = getByRole('alert');
    expect(secretFriend).toBeInTheDocument();
  });
});
