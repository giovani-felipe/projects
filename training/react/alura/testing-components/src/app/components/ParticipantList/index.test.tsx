import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import { RecoilRoot } from 'recoil';
import ParticipantListComponent from '.';
import { useParticipantList } from '../../state/hooks/useParticipantList';

vi.mock('../../state/hooks/useParticipantList', () => {
  return { useParticipantList: vi.fn() };
});

describe('ParticipantListComponent', () => {
  describe('empty list', () => {
    beforeEach(() => {
      vi.mocked(useParticipantList).mockReturnValue([]);
    });

    it('an empty participant list', () => {
      const { queryAllByRole } = render(
        <RecoilRoot>
          <ParticipantListComponent />
        </RecoilRoot>
      );

      const items = queryAllByRole('listitem');
      expect(items).toHaveLength(0);
    });
  });

  describe('filled list', () => {
    const participants = ['Giovani', 'Felipe'];
    beforeEach(() => {
      vi.mocked(useParticipantList).mockReturnValue(participants);
    });
    it('a filled participant list', () => {
      const { queryAllByRole } = render(
        <RecoilRoot>
          <ParticipantListComponent />
        </RecoilRoot>
      );

      const items = queryAllByRole('listitem');
      expect(items).toHaveLength(participants.length);
    });
  });
});
