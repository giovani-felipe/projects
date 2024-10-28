import api from './api';
import { buscaTransacoes, salvaTransacao } from './transacoes';

jest.mock('./api');

const mockTransacoes = [
  {
    id: 1,
    transacao: 'Depópsito',
    valor: '100',
    data: '22/11/2022',
    mes: 'Novembro',
  },
];

const mockRequisicao = (retorno) =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: retorno,
      });
    }, 200);
  });

const mockRequisicaoErro = () =>
  new Promise((_, reject) => {
    setTimeout(() => {
      reject();
    }, 200);
  });

const mockRequisicaoPost = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        status: 201,
      });
    }, 200);
  });
};

describe('Requisições para API', () => {
  test('Deve retornar uma lista de transações', async () => {
    api.get.mockImplementation(() => mockRequisicao(mockTransacoes));

    const transacoes = await buscaTransacoes();
    expect(transacoes).toEqual(mockTransacoes);
    expect(api.get).toHaveBeenCalledWith('/transacoes');
  });

  test('Deve retornar uma lista vazia quanto a requisição falhar', async () => {
    api.get.mockImplementation(() => mockRequisicaoErro());

    const transacoes = await buscaTransacoes();
    expect(transacoes).toEqual([]);
    expect(api.get).toHaveBeenCalledWith('/transacoes');
  });

  test('Deve retornar um status 201 - (Created) após uma requisição POST', async () => {
    api.post.mockImplementation(() => mockRequisicaoPost());
    const status = await salvaTransacao(mockTransacoes[0]);
    expect(status).toBe(201);
    expect(api.post).toHaveBeenCalledWith('/transacoes', mockTransacoes[0]);
  });
});
