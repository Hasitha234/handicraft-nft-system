import Link from 'next/link';
import Button from '@/components/Shared/Button';

export default function HomePage() {
  const features = [
    {
      title: 'Classification',
      description: 'Classify handicrafts as Traditional, Fusion, or Modern',
      href: '/classification',
      icon: '🎨',
    },
    {
      title: 'Design Generator',
      description: 'Generate AI-powered fusion designs',
      href: '/design-generator',
      icon: '✨',
    },
    {
      title: 'User Preferences',
      description: 'Collect user preferences through interactive gallery',
      href: '/preferences',
      icon: '👥',
    },
    {
      title: 'Analytics',
      description: 'View insights and market trends',
      href: '/analytics',
      icon: '📊',
    },
  ];

  return (
    <div className="min-h-screen bg-primary">
      <div className="containerpadding container mx-auto py-12 md:py-20">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="title text-blackbrown mb-6">
            AI-Assisted Design System
          </h1>
          <p className="description text-blackbrown max-w-3xl mx-auto text-lg mb-8">
            Empowering Sri Lankan handicraft artisans with AI-powered design recommendations
            and market insights. Classify, generate, and analyze designs to bridge traditional
            craftsmanship with modern market demands.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 mb-12">
          {features.map((feature) => (
            <Link
              key={feature.href}
              href={feature.href}
              className="bg-primary border-2 border-lightbrown rounded-lg p-6 hover:border-secondarybrown transition-all duration-200 hover:shadow-lg"
            >
              <div className="flex items-start space-x-4">
                <span className="text-4xl">{feature.icon}</span>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-blackbrown mb-2">
                    {feature.title}
                  </h3>
                  <p className="description text-blackbrown">
                    {feature.description}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Stats Section */}
        <div className="bg-lightbrown/30 border border-lightbrown rounded-lg p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-secondarybrown mb-2">79.25%</div>
              <div className="description text-blackbrown">Classification Accuracy</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-secondarybrown mb-2">258</div>
              <div className="description text-blackbrown">Training Images</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-secondarybrown mb-2">3</div>
              <div className="description text-blackbrown">Design Categories</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
