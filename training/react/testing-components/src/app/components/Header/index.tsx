// src/componentes/Cabecalho/index.tsx
import './style.css';

const HeaderComponent = () => {
  return (
    <header className="header">
      <div
        className="image-logo"
        role="img"
        aria-label="Sweepstakes logo"
      ></div>
      <img
        className="participant"
        src="/assets/imagens/participant.png"
        alt="Participant with gift in hand"
      />
    </header>
  );
};

export default HeaderComponent;
