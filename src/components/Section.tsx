interface SectionProps {
  title: string;
  viewAllLink?: string;
  viewAllText?: string;
  children: React.ReactNode;
}

export default function Section({ title, viewAllLink, viewAllText = "View all →", children }: SectionProps) {
  return (
    <section className="mb-16">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900">{title}</h2>
        {viewAllLink && (
          <a href={viewAllLink} className="text-blue-600 hover:text-blue-800 font-medium">
            {viewAllText}
          </a>
        )}
      </div>
      {children}
    </section>
  );
}