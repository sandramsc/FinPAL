import { feedback } from "../constants";
import FeedbackCard from "./FeedbackCard";
import styles, { layout } from "../style";

const Testimonials = () => (

  <section id="clients" className={`${styles.paddingY} ${styles.flexCenter} flex-col relative `}>
    <div className="my-6">
      <h2 className={styles.heading2}>
        Features
      </h2>
    </div>

    <div className="absolute z-[0] w-[30%] h-[30%] -right-[25%] rounded-full blue__gradient bottom-40" />

    <div className="flex flex-wrap sm:justify-center justify-center w-full feedback-container relative z-[1]">
      {feedback.map((card) => <FeedbackCard key={card.id} {...card} />)}
    </div>
  </section>
);

export default Testimonials;
