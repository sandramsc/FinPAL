import { clients } from "../constants";
import styles from "../style";

const Clients = () => (
  <section className={`${styles.flexCenter} ${styles.flexCenter} flex-col relative my-4`}>
    <div className="my-2">
      <h2 className={styles.heading2}>
       15+ Integrations
      </h2>
    </div>
    <div className={`${styles.flexCenter} flex-wrap w-full`}>
      {clients.map((client) => (
        <div key={client.id} className={`flex-1 ${styles.flexCenter} sm:min-w-[192px] min-w-[120px] m-5`}>
          <img src={client.logo} alt="client_logo" className="sm:w-[1100px] w-[100px] object-contain" />
        </div>
      ))}
    </div>
  </section>
);

export default Clients;
