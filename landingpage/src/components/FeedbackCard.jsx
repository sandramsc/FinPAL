const FeedbackCard = ({ content, name, title, img }) => (
  <div className="flex justify-between flex-col px-10 py-8 rounded-[20px]  max-w-[300px] md:mr-10 sm:mr-5 mr-0 my-5 feedback-card">
     <img src={img} alt={name} className="w-[48px] h-[48px] rounded-full" />
    <h4 className="font-poppins font-semibold text-[18px] leading-[24px] text-white my-6">
          {name}
    </h4>
    <p className="font-poppins font-normal text-[16px] leading-[20.4px] text-white">
      {content}
    </p>
    <p className="font-poppins font-normal text-[14px] leading-[20px] text-dimWhite my-3">
          {title}
    </p>
  </div>
);


export default FeedbackCard;
