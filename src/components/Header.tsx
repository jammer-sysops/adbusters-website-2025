interface HeaderProps {
  title?: string;
  subtitle?: string;
  showNavigation?: boolean;
}

export default function Header({ 
  title = "Adbusters", 
  subtitle = "Journal of the mental environment",
  showNavigation = true 
}: HeaderProps) {
  return (
    <header className="text-center mb-16">
      <h1 className="text-5xl font-bold text-gray-900 mb-4">{title}</h1>
      {subtitle && <p className="text-xl text-gray-600">{subtitle}</p>}
      
      {showNavigation && (
        <nav className="mt-8">
          <a 
            href="/articles" 
            className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
          >
            Browse Articles
          </a>
        </nav>
      )}
    </header>
  );
}