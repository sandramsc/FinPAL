import { telegrambot } from "../assets";
import styles, { layout } from "../style";
import Button from "./Button";

const CardDeal = () => (
  <section className={layout.section}>
    <div className={layout.sectionInfo}>
      <h2 className={styles.heading2}>
        Explore our telegram bot
      </h2>
      <p className={`${styles.paragraph} max-w-[470px] mt-5`}>
      Build on FinPAL to create innovative and streamlined customer experiences.
      </p>

      <Button styles={`mt-10`} />
    </div>

    <div className={layout.sectionImg}>
      <img src={telegrambot} alt="billing" className="w-[70%] h-[90%]" />
    </div>
  </section>
);

export default CardDeal;
