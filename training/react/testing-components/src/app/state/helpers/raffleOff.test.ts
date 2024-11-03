import { raffleOff } from './raffleOff';

describe('raffleOff', () => {
  it('each participant cannot sweepstake their own name', () => {
    const participants = ['Giovani', 'Felipe', 'Miguel', 'Michelle'];
    const sweepstake = raffleOff(participants);

    participants.forEach((participant) => {
      const friendSecret = sweepstake.get(participant);
      expect(friendSecret).not.toEqual(participant);
    });
  });
});
