import { useState, useEffect, useRef } from 'react';

interface NavItem {
  text: string;
  href: string;
  priority?: number;
  isPunk?: boolean;
}


const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [shouldShake, setShouldShake] = useState(false);
  const navRef = useRef<HTMLDivElement>(null);

  const leftNavItems: NavItem[] = [
    { text: 'Manifesto', href: 'https://subscribe.adbusters.org/products/a-manifesto-for-world-revolution', priority: 1 },
    { text: 'Join Us', href: '/manifesto', priority: 2 },
    { text: 'Mindbombs', href: '/fundraising', priority: 3 },
  ];

  const rightNavItems: NavItem[] = [
    { text: 'Jams', href: '/spoof-ads', priority: 3 },
    { text: 'Culture Shop', href: 'https://subscribe.adbusters.org/', priority: 0 },
  ];


  const mobileMenuItems: NavItem[] = [
    { text: 'Culture Shop', href: 'https://subscribe.adbusters.org/' },
    { text: 'MANIFESTO', href: 'https://subscribe.adbusters.org/products/a-manifesto-for-world-revolution', isPunk: true },
    { text: 'Join Us', href: '/manifesto', isPunk: true },
    { text: 'Jams', href: '/spoof-ads' },
    { text: 'Tools', href: '/downloads' },
    { text: 'About Us', href: '/about-us' },
  ];

  // Menu icon shake effect
  useEffect(() => {
    if (typeof window !== 'undefined' && !sessionStorage.getItem('menuSeen')) {
      const timer = setTimeout(() => {
        if (!isMobileMenuOpen) {
          setShouldShake(true);
          setTimeout(() => setShouldShake(false), 500);
          sessionStorage.setItem('menuSeen', 'true');
        }
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isMobileMenuOpen]);


  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="adbusters-navbar relative w-full z-[1000]" style={{ backgroundColor: 'var(--ad-navbar-bg)', color: 'var(--ad-navbar-text)' }} ref={navRef}>
      <div className="relative">
        {/* Main navigation bar */}
        <nav className="navbar-border relative px-8 py-4 mb-5 md:px-8 md:py-4" style={{ backgroundColor: 'var(--ad-navbar-bg)', color: 'var(--ad-navbar-text)' }}>
          <div className="flex items-center w-full">
            {/* Left section */}
            <div className="flex-1 flex justify-start items-center gap-4 hidden md:flex">
              {leftNavItems.map((item) => (
                <div key={item.text} className="nav-item" data-priority={item.priority}>
                  <a
                    href={item.href}
                    className="nav-link-underline relative font-bold uppercase tracking-wider px-2 py-1 transition-all duration-200 hover:-translate-y-0.5 hover:skew-x-[-3deg]"
                    style={{ color: 'var(--ad-navbar-text)' }}
                  >
                    {item.text}
                  </a>
                </div>
              ))}
            </div>

            {/* Logo/Brand Section (Center) */}
            <div className="flex-none flex justify-center items-center md:flex-auto">
              <a href="/" className="flex items-center no-underline">
                <img
                  src="https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/654188a0558a5db58bb21bf7_Adbusters_turtle_logo.png"
                  alt="Adbusters logo"
                  className="w-8 md:w-12 h-auto transform -rotate-[5deg] mix-blend-darken"
                />
                <img
                  src="https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/685c43a937cb00efdff0dba0_adbusters%20name%20thick%20pen%20font.jpg"
                  alt="Adbusters"
                  className="w-[120px] md:w-[140px] max-w-full h-auto ml-2 mix-blend-darken"
                />
              </a>
            </div>

            {/* Right section */}
            <div className="flex-1 flex justify-end items-center gap-2 md:gap-3">
              <div className="hidden md:flex items-center gap-3">
                {rightNavItems.filter(item => item.priority !== 0).map((item) => (
                  <div key={item.text} className="nav-item" data-priority={item.priority}>
                    <a
                      href={item.href}
                      className="nav-link-underline relative font-bold uppercase tracking-wider px-2 py-1 transition-all duration-200 hover:-translate-y-0.5 hover:skew-x-[-3deg]"
                      style={{ color: 'var(--ad-navbar-text)' }}
                    >
                      {item.text}
                    </a>
                  </div>
                ))}


                <div className="nav-item" data-priority="0">
                  <a
                    href="https://subscribe.adbusters.org/"
                    className="nav-link-underline relative font-bold uppercase tracking-wider px-2 py-1 transition-all duration-200 hover:-translate-y-0.5 hover:skew-x-[-3deg]"
                    style={{ color: 'var(--ad-navbar-text)' }}
                  >
                    Culture Shop
                  </a>
                </div>
              </div>

              {/* Menu Toggle Button */}
              <div className="nav-item menu-container">
                <button
                  onClick={toggleMobileMenu}
                  className="flex justify-center items-center p-2 ml-2 relative transition-transform duration-200 hover:scale-110"
                  aria-label="Toggle navigation menu"
                  aria-expanded={isMobileMenuOpen}
                >
                  <img
                    src="https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/685c4b6663b6d0ce3074f5d7_mobile%20menu%20hand%20drawn.jpg"
                    alt="Menu"
                    className={`w-8 h-auto object-contain ${shouldShake ? 'shake' : ''}`}
                  />
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Mobile Menu Panel */}
        <ul className={`mobile-menu-border fixed top-0 w-max min-w-[200px] h-screen px-8 pt-16 pb-8 transition-all duration-500 ease-out z-[1001] list-none ${
          isMobileMenuOpen ? 'right-0 translate-x-0' : '-right-full translate-x-full'
        }`} style={{ backgroundColor: 'var(--ad-navbar-bg)' }}>
          <div className="nav-item menu-container mb-8">
            <button
              onClick={toggleMobileMenu}
              className="flex justify-center items-center p-2 relative transition-transform duration-200 hover:scale-110"
              aria-label="Close navigation menu"
              aria-expanded={isMobileMenuOpen}
            >
              <img
                src="https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/685c4b6663b6d0ce3074f5d7_mobile%20menu%20hand%20drawn.jpg"
                alt="Menu"
                className="w-8 h-auto object-contain"
              />
            </button>
          </div>

          {mobileMenuItems.map((item) => (
            <li key={item.text} className="my-5">
              <a
                href={item.href}
                className={`font-bold uppercase tracking-wider text-lg transition-all duration-300 ${
                  item.isPunk 
                    ? 'punk-link relative overflow-hidden transform -rotate-1 font-black hover:skew-x-[-5deg]' 
                    : 'hover:-translate-y-0.5 hover:skew-x-[-3deg]'
                }`}
                style={{ 
                  color: item.isPunk ? 'var(--ad-navbar-accent)' : 'var(--ad-navbar-text)',
                  fontFamily: item.isPunk ? 'Impact, Arial Black, sans-serif' : 'inherit'
                }}
              >
                {item.text}
              </a>
            </li>
          ))}

        </ul>
      </div>
    </div>
  );
};

export default Navbar;