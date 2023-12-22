import { useState } from "react";
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';

import { close, logo, menu } from "../assets";
import { navLinks } from "../constants";
import "../index.css"

const Navbar = () => {
  const [active, setActive] = useState("Home");
  const [toggle, setToggle,toggleMenu, setToggleMenu] = useState(false);

  return (
    <nav className="w-full flex py-6 justify-between items-center navbar">
      <img src={logo} alt="hoobank" className="w-[130px] h-[58px]" />
 
      <ul className="list-none sm:flex hidden justify-center items-center flex-1">
        {navLinks.map((nav, index) => (
          <li
            key={nav.id}
            className={`font-poppins font-normal cursor-pointer text-[16px] ${
              active === nav.title ? "text-white" : "text-dimWhite"
            } ${index === navLinks.length - 1 ? "mr-0" : "mr-10"}`}
            onClick={() => setActive(nav.title)}
          >
            <a href={`#${nav.id}`}>{nav.title}</a>
          </li>
          
        ))}
      </ul>

      <div className="gpt3__navbar">
<div className="gpt3__navbar-sign">
<a href="https://finpaldash.vercel.app/dashboard/user_id/test/start_date/20230101/end_date/20231212">
  <p>Sign in</p>
  </a>
  <a href="https://finpaldash.vercel.app/dashboard/user_id/test/start_date/20230101/end_date/20231212">
  <button type="button">Sign up</button>
  </a>
</div>
<div className="gpt3__navbar-menu">
  {toggleMenu
    ? <RiCloseLine color="#fff" size={27} onClick={() => setToggleMenu(false)} />
    : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />}
  {toggleMenu && (
    <a href="https://finpaldash.vercel.app/">
  <div className="gpt3__navbar-menu_container scale-up-center">
    <div className="gpt3__navbar-menu_container-links-sign">
      <a href="">
      <p>Sign in</p>
      </a>
      <a>
      <button type="button">Sign up</button>
      </a>
    </div>
  </div>
  </a>
  )}
</div>
</div>
    

      <div className="sm:hidden flex flex-1 justify-center items-center">
        <img
          src={toggle ? close : menu}
          alt="menu"
          className="w-[28px] h-[28px] object-contain"
          onClick={() => setToggle(!toggle)}
        />

        <div
          className={`${
            !toggle ? "hidden" : "flex"
          } p-6 bg-black-gradient absolute top-20 right-0 mx-4 my-2 min-w-[140px] rounded-xl sidebar`}
        >
          <ul className="list-none flex justify-center items-start flex-1 flex-col">
            {navLinks.map((nav, index) => (
              <li
                key={nav.id}
                className={`font-poppins font-medium cursor-pointer text-[16px] ${
                  active === nav.title ? "text-white" : "text-dimWhite"
                } ${index === navLinks.length - 1 ? "mb-0" : "mb-4"}`}
                onClick={() => setActive(nav.title)}
              >
                <a href={`#${nav.id}`}>{nav.title}</a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
