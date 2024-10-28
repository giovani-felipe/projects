const { renderHook, act } = require('@testing-library/react');
const { buscaTransacoes } = require('../services/transacoes');
const { default: useListaTransacoes } = require('./useListaTransacoes');

jest.mock('../services/transacoes');

const mockTransacoes = [
  {
    id: 1,
    transacao: 'Depópsito',
    valor: '100',
    data: '22/11/2022',
    mes: 'Novembro',
  },
];

describe('hooks/useListaTransacoes', () => {
  test('Deve retornar uma lista de transações e uma função que a atualiza', async () => {
    buscaTransacoes.mockImplementation(() => mockTransacoes);

    const { result } = renderHook(() => useListaTransacoes());
    expect(result.current[0]).toEqual([]);
    await act(async () => {
      result.current[1]();
    });

    expect(result.current[0]).toEqual(mockTransacoes);
  });
});
