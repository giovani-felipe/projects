import Card from '../components/Card';
import FooterComponent from '../components/Footer';
import FormComponent from '../components/Form';
import ParticipantListComponent from '../components/ParticipantList';

const ConfigurationPage = () => {
  return (
    <Card>
      <section>
        <h2>Let's go started!</h2>
        <FormComponent />
        <ParticipantListComponent />
        <FooterComponent />
      </section>
    </Card>
  );
};

export default ConfigurationPage;
