import ArticleCard from './ArticleCard';

interface Article {
  slug: string;
  data: {
    title: string;
    publishedOn?: string;
    featuredImage?: string;
  };
  body: string;
}

interface ArticleGridProps {
  articles: Article[];
  showExcerpts?: boolean;
}

export default function ArticleGrid({ articles, showExcerpts = false }: ArticleGridProps) {
  const getExcerpt = (content: string, maxLength: number = 200) => {
    // Remove markdown formatting and get plain text
    const plainText = content.replace(/[#*`]/g, '').replace(/\n+/g, ' ').trim();
    if (plainText.length <= maxLength) return plainText;
    return plainText.substring(0, maxLength).trim() + '...';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {articles.map((article) => (
        <ArticleCard
          key={article.slug}
          title={article.data.title}
          slug={article.slug}
          publishedOn={article.data.publishedOn}
          excerpt={showExcerpts ? getExcerpt(article.body) : undefined}
          featuredImage={article.data.featuredImage}
        />
      ))}
    </div>
  );
}