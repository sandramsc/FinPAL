import { telegrambot } from "../assets";
import styles, { layout } from "../style";
import Scan_Button from "./Scan_Button";

const CardDeal = () => (
  <section className={layout.section}>
    <div className={layout.sectionInfo}>
      <h2 className={styles.heading2}>
        Explore our Telegram bot
      </h2>
      <Scan_Button styles={`mt-10`} />
    </div>

    <div className={layout.sectionImg}>
      <img src={telegrambot} alt="billing" className="w-[70%] h-[100%]" />
    </div>
  </section>
);

export default CardDeal;
