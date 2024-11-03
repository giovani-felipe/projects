import CardComponent from '../components/Card';
import FooterComponent from '../components/Footer';
import FormComponent from '../components/Form';
import ParticipantListComponent from '../components/ParticipantList';

const ConfigurationPage = () => {
  return (
    <CardComponent>
      <section>
        <h2>Let's go started!</h2>
        <FormComponent />
        <ParticipantListComponent />
        <FooterComponent />
      </section>
    </CardComponent>
  );
};

export default ConfigurationPage;
