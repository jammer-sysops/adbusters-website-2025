interface ArticleCardProps {
  title: string;
  slug: string;
  publishedOn?: string;
  excerpt?: string;
  featuredImage?: string;
}

export default function ArticleCard({ title, slug, publishedOn, excerpt, featuredImage }: ArticleCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <article className="group cursor-pointer">
      <a href={`/articles/${slug}`} className="block">
        <div className="space-y-4">
          {featuredImage && (
            <div className="aspect-video overflow-hidden rounded-lg bg-gray-100">
              <img 
                src={featuredImage} 
                alt={title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>
          )}
          
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-gray-600 transition-colors line-clamp-2">
              {title}
            </h3>
            
            {publishedOn && (
              <time dateTime={publishedOn} className="text-sm text-gray-500">
                {formatDate(publishedOn)}
              </time>
            )}

            {excerpt && (
              <p className="text-gray-600 line-clamp-3">
                {excerpt}
              </p>
            )}
          </div>
        </div>
      </a>
    </article>
  );
}