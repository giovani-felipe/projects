import { fireEvent, render } from '@testing-library/react';
import { RecoilRoot } from 'recoil';
import FooterComponent from '.';
import '@testing-library/jest-dom';
import { useParticipantList } from '../../states/hooks/useParticipantList';

vi.mock('../../states/hooks/useParticipantList', () => {
  return {
    useParticipantList: vi.fn(),
  };
});

const useNavigateMock = vi.fn();
vi.mock('react-router-dom', () => {
  return {
    useNavigate: () => useNavigateMock,
  };
});

describe('FooterComponent', () => {
  describe('empty list', () => {
    beforeEach(() => {
      vi.mocked(useParticipantList).mockReturnValue([]);
    });
    it('when there are not enough participants', () => {
      const { getByRole } = render(
        <RecoilRoot>
          <FooterComponent />
        </RecoilRoot>
      );

      const button = getByRole('button');

      expect(button).toBeDisabled();
    });
  });
  describe('filled list', () => {
    const participants = ['Giovani', 'Felipe', 'Miguel'];
    beforeEach(() => {
      vi.mocked(useParticipantList).mockReturnValue(participants);
    });
    it('when there are not enough participants', () => {
      const { getByRole } = render(
        <RecoilRoot>
          <FooterComponent />
        </RecoilRoot>
      );

      const button = getByRole('button');

      expect(button).not.toBeDisabled();
    });

    it('joking has been started', () => {
      const { getByRole } = render(
        <RecoilRoot>
          <FooterComponent />
        </RecoilRoot>
      );

      const button = getByRole('button');

      fireEvent.click(button);

      expect(useNavigateMock).toHaveBeenCalledTimes(1);
    });
  });
});
