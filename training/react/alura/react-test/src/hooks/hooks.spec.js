const { renderHook } = require('@testing-library/react');
const { useEffect } = require('react');
const { useState } = require('react');

test('Hooks', () => {
  const { result } = renderHook(() => {
    const [nome, setNome] = useState('');
    useEffect(() => {
      setNome('Alice');
    }, []);

    return nome;
  });

  expect(result.current).toBe('Alice');
});
