import styles from "../style";
import Button from "./Button";

const CTA = () => (
  <section className={`${styles.flexCenter} ${styles.marginY} ${styles.padding} sm:flex-row flex-col bg-black-gradient-2 rounded-[20px] box-shadow`}>
    <div className="flex-1 flex flex-col">
      <h4 className={styles.heading2}>Ready to effortlessly manage <br className="sm:block hidden" />{" "}
      <span> your receipts and expenses?</span>{" "}
      
      </h4>
      <p className={`${styles.paragraph} max-w-[700px] mt-5`}>
      Enter your contact info to maximize your finances with FinPAL's innovative time-saving spend tools.
      </p>
    </div>

    <div className={`${styles.flexCenter} sm:ml-10 ml-0 sm:mt-0 mt-10`}>
      <Button />
    </div>
  </section>
  
);

export default CTA;
