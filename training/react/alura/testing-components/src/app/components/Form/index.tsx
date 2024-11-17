import { FormEvent, useRef, useState } from 'react';
import { useParticipantAdd } from '../../state/hooks/useParticipantAdd';
import useErrorMessage from '../../state/hooks/useErrorMessage';

import './style.css';

const FormComponent = () => {
  const [name, setName] = useState('');

  const inputRef = useRef<HTMLInputElement>(null);
  const errorMessage = useErrorMessage();
  const handleAddParticipant = useParticipantAdd();

  const addParticipant = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleAddParticipant(name);
    setName('');
    inputRef.current?.focus();
  };

  return (
    <form onSubmit={addParticipant}>
      <div className="group-input-btn">
        <input
          ref={inputRef}
          type="text"
          placeholder="Insert the participants' names"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        <button disabled={!name} type="submit">
          Add
        </button>
      </div>
      {errorMessage && (
        <p role="alert" className="alert error">
          {errorMessage}
        </p>
      )}
    </form>
  );
};

export default FormComponent;
