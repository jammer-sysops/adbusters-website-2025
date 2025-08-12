interface FooterLink {
  text: string;
  href: string;
}

interface SocialLink {
  platform: string;
  href: string;
  icon: string;
}

const Footer = () => {
  const subscriptionLinks: FooterLink[] = [
    { text: 'Subscribe to our magazine', href: 'https://subscribe.adbusters.org/pages/subscriptions' },
    { text: 'Get our next issue for $5', href: 'https://subscribe.adbusters.org/products/ab-168-preorder' },
    { text: 'Become a Friend of the foundation', href: 'https://subscribe.adbusters.org/products/friend-of-the-foundation-package' },
    { text: 'Become a lifetimer', href: 'https://subscribe.adbusters.org/products/lifetime-subscription-and-get-a-t-shirt' },
    { text: 'Donate to our cause', href: 'https://subscribe.adbusters.org/pages/donate' },
  ];

  const aboutLinks: FooterLink[] = [
    { text: 'Culture Shop', href: 'https://subscribe.adbusters.org/' },
    { text: 'About Us', href: '/about-us' },
    { text: 'Spoof ads', href: '/spoof-ads' },
    { text: 'Psychomedia', href: '/psychomedia' },
    { text: "Kalle's Mindbombs", href: 'https://www.adbusters.org/podcast/hummingbird' },
    { text: 'Downloads', href: '/downloads' },
  ];

  const socialLinks: SocialLink[] = [
    { platform: 'Twitter', href: 'https://twitter.com/Adbusters?s=20&t=uSG31XPRSHW-5m9WAH1GuQ', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/5ee3cd1b187c8355fb642a88_twitter.svg' },
    { platform: 'Instagram', href: 'https://www.instagram.com/adbusters.magazine/?hl=en', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/5ee3cd28851b1a9c5e710567_instagram.svg' },
    { platform: 'Facebook', href: 'https://www.facebook.com/adbusters/', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/5ee3cce918269a64c83bc8f9_facebook.svg' },
    { platform: 'Reddit', href: 'https://www.reddit.com/r/adbusters/', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/64bb12a2292b8b83528f79f8_5279117_forum_reddit_reddit%20logo_icon.png' },
    { platform: 'TikTok', href: 'https://www.tiktok.com/@adbustersmedia', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/64bb12c737717a1955e11abd_7693325_tiktok_social%20media_logo_apps_icon.png' },
    { platform: 'YouTube', href: 'https://www.youtube.com/adbusters', icon: 'https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/5ab163de19104911e58a64be_001-youtube.png' },
  ];


  return (
    <footer className="footer-bg bg-cover bg-center bg-repeat relative font-serif" style={{ 
      backgroundImage: 'url("https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/64655d3802822b69dd67bd5f_bg_warm2_paper_texture_2023_1080x702.jpg")',
      borderTop: '1px solid #e4ebf3'
    }}>
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="py-12 grid grid-cols-1 lg:grid-cols-6 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <a href="/" className="inline-block mb-4">
              <img
                src="https://cdn.prod.website-files.com/5ab163de19104964ce8a64b9/62ba182620d42c4adbcb90cf_ADBUSTERS_nobg_black_240x72.png"
                alt="Adbusters"
                className="h-12 w-auto"
              />
            </a>
            <p className="text-sm leading-relaxed mb-4">
              <strong>Adbusters</strong> receives <strong>zero funding</strong> from advertising, corporate sponsorship or foundation grants. We are entirely reader-supported. When you{' '}
              <a href="https://subscribe.adbusters.org/" className="font-bold underline">
                subscribe
              </a>{' '}
              to Adbusters, you are joining a <strong>network of artists and activists</strong> committed to{' '}
              <strong>speaking truth</strong> to power without reservation.
            </p>
            <div className="mb-6">
              <a
                href="/manifesto"
                className="inline-block bg-gray-800 text-white px-4 py-2 font-bold uppercase text-sm hover:bg-gray-900 transition-colors"
              >
                Join the Third Force
              </a>
            </div>
          </div>

          {/* Subscription Links */}
          <div className="lg:col-span-2">
            <div className="space-y-3 max-w-xs">
              {subscriptionLinks.map((link) => (
                <a
                  key={link.text}
                  href={link.href}
                  className="block text-sm font-bold hover:underline transition-colors"
                >
                  {link.text}
                </a>
              ))}
            </div>
          </div>

          {/* About Links */}
          <div className="lg:col-span-1">
            <div className="space-y-3">
              {aboutLinks.map((link) => (
                <a
                  key={link.text}
                  href={link.href}
                  className="block text-sm font-bold hover:underline transition-colors"
                >
                  {link.text}
                </a>
              ))}
            </div>
          </div>

          {/* Social Links */}
          <div className="lg:col-span-1">
            <div className="grid grid-cols-2 gap-2 max-w-[80px]">
              {socialLinks.map((social) => (
                <a
                  key={social.platform}
                  href={social.href}
                  className="w-6 h-6 flex items-center justify-center hover:opacity-70 transition-opacity"
                  title={social.platform}
                >
                  <img
                    src={social.icon}
                    alt={social.platform}
                    className="w-full h-full object-contain"
                  />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-gray-300 py-4">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm font-serif">
            © 2025 Adbusters Media Foundation -{' '}
            <a href="https://www.adbusters.org/privacy-policy" className="underline">
              Privacy Policy
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;