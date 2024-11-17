import { render } from '@testing-library/react';
import { RecoilRoot } from 'recoil';
import ConfigurationPage from './ConfigurationPage';

const useNavigateMock = vi.fn();
vi.mock('react-router-dom', () => {
  return {
    useNavigate: () => useNavigateMock,
  };
});

describe('ConfigurationPage', () => {
  it('should be rendered correctly', () => {
    const { container } = render(
      <RecoilRoot>
        <ConfigurationPage />
      </RecoilRoot>
    );

    expect(container).toMatchSnapshot();
  });
});
