import '@testing-library/jest-dom';
import { fireEvent, render, act } from '@testing-library/react';
import FormComponent from '.';
import { RecoilRoot } from 'recoil';

describe('FormComponent', () => {
  it('when the input is empty, new participants cannot be inserted', () => {
    const { getByPlaceholderText, getByRole } = render(
      <RecoilRoot>
        <FormComponent />
      </RecoilRoot>
    );

    expect(
      getByPlaceholderText("Insert the participants' names")
    ).toBeInTheDocument();
    expect(getByRole('button')).toBeDisabled();
  });

  it('add a participant when the name has been filled in', () => {
    const { getByPlaceholderText, getByRole } = render(
      <RecoilRoot>
        <FormComponent />
      </RecoilRoot>
    );

    const input = getByPlaceholderText("Insert the participants' names");
    const button = getByRole('button');

    fireEvent.change(input, {
      target: { value: 'Giovani Santos' },
    });
    fireEvent.click(button);

    expect(input).toHaveFocus();
    expect(input).toHaveValue('');
  });

  it('duplicate names cannot be added in the list', () => {
    const { getByPlaceholderText, getByRole } = render(
      <RecoilRoot>
        <FormComponent />
      </RecoilRoot>
    );

    const input = getByPlaceholderText("Insert the participants' names");
    const button = getByRole('button');

    fireEvent.change(input, {
      target: { value: 'Giovani Santos' },
    });
    fireEvent.click(button);

    fireEvent.change(input, {
      target: { value: 'Giovani Santos' },
    });
    fireEvent.click(button);

    const errorMessage = getByRole('alert');

    expect(errorMessage.textContent).toBe('Duplicate names are not allowed');
  });

  it('error message should disappear after 3s', () => {
    vi.useFakeTimers();
    const { getByPlaceholderText, getByRole, queryByRole } = render(
      <RecoilRoot>
        <FormComponent />
      </RecoilRoot>
    );

    const input = getByPlaceholderText("Insert the participants' names");
    const button = getByRole('button');

    fireEvent.change(input, {
      target: { value: 'Giovani Santos' },
    });
    fireEvent.click(button);

    fireEvent.change(input, {
      target: { value: 'Giovani Santos' },
    });
    fireEvent.click(button);

    expect(getByRole('alert')).toBeInTheDocument();

    act(() => {
      vi.runAllTimers();
    });

    const errorMessageAfter = queryByRole('alert');
    expect(errorMessageAfter).toBeNull();
  });
});
