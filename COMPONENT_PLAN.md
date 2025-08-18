# Adbusters Website Component Development Plan

**Reference Site**: https://www.adbusters.org/ (analyze this for design patterns and component examples)

## Overview
This plan outlines the components needed to replicate the punk aesthetic and activist functionality of the original Adbusters website within our Astro/React stack.

## Component Inventory

### Current Components (Existing)
- **ArticleGrid.astro** - Grid layout for articles
- **Footer.astro** - Site footer
- **Header.tsx** - Site header
- **Navbar.tsx** - Navigation with punk aesthetic
- **RandomBrush.astro/tsx** - Brush stroke effects
- **Section.tsx** - Section wrapper

### New Components Needed

#### 1. **HeroCampaign.tsx**
Full-width campaign spotlight component
- **Features**:
  - Large background images/videos
  - Overlaid text with punk typography
  - YouTube/Vimeo embed support
  - Call-to-action buttons with hand-drawn borders
  - Responsive scaling
  - Optional countdown timer for time-sensitive campaigns
- **Props**:
  - `backgroundImage/Video`: string
  - `title`: string
  - `subtitle`: string
  - `ctaButtons`: Array<{text, link, style}>
  - `mediaEmbed`: string (optional)
  - `countdown`: Date (optional)

#### 2. **MediaBlock.tsx**
Flexible media embedding component
- **Features**:
  - YouTube/Vimeo video embeds
  - Image galleries with lightbox
  - Audio player support
  - Lazy loading for performance
  - Caption support
- **Props**:
  - `type`: 'video' | 'gallery' | 'audio'
  - `source`: string | string[]
  - `caption`: string
  - `autoplay`: boolean

#### 3. **Sidebar.tsx**
Sticky sidebar for campaigns and promotions
- **Features**:
  - Sticky positioning on desktop
  - Campaign promotion cards
  - Newsletter signup form
  - Social media feed integration
  - Donation/support buttons
  - Recent actions/petitions
- **Props**:
  - `campaigns`: Array<Campaign>
  - `showNewsletter`: boolean
  - `socialFeeds`: Array<string>
  - `position`: 'left' | 'right'

#### 4. **CampaignCard.tsx**
Visual impact card for campaigns (different from ArticleCard)
- **Features**:
  - Large image backgrounds
  - Bold typography overlays
  - Hover animations (glitch effects)
  - Category tags with punk styling
  - Progress indicators for fundraising
  - Share buttons
- **Props**:
  - `image`: string
  - `title`: string
  - `description`: string
  - `tags`: string[]
  - `progress`: number (optional)
  - `targetAmount`: number (optional)

#### 5. **QuoteBlock.tsx**
Pull quotes and testimonials
- **Features**:
  - Large typography display
  - Hand-drawn quotation marks
  - Author attribution
  - Social media share links
  - Animated entrance effects
- **Props**:
  - `quote`: string
  - `author`: string
  - `source`: string (optional)
  - `shareable`: boolean

#### 6. **CallToAction.tsx**
Versatile CTA component
- **Features**:
  - Multiple style variations (banner, inline, popup, floating)
  - Animated borders/backgrounds
  - Countdown timers
  - Progress bars
  - Form integration support
- **Props**:
  - `style`: 'banner' | 'inline' | 'popup' | 'floating'
  - `text`: string
  - `action`: string | Function
  - `countdown`: Date (optional)
  - `progress`: number (optional)

#### 7. **TimelineEvent.tsx**
Campaign timeline display
- **Features**:
  - Vertical timeline layout
  - Date markers
  - Event cards with images
  - Expandable details
- **Props**:
  - `events`: Array<{date, title, description, image}>
  - `orientation`: 'vertical' | 'horizontal'

#### 8. **PetitionForm.tsx**
Action/petition signing component
- **Features**:
  - Form validation
  - Signature counter
  - Progress to goal
  - Share after signing
  - Email opt-in
- **Props**:
  - `petitionId`: string
  - `targetSignatures`: number
  - `currentSignatures`: number
  - `fields`: Array<FormField>

## Component Enhancements

### Existing Components to Enhance

1. **Navbar.tsx**
   - Add dropdown menu support
   - Implement search functionality
   - Add campaign ticker/banner
   - Improve mobile menu animations

2. **Header.tsx**
   - Add hero variations
   - Support video backgrounds
   - Add parallax effects
   - Implement typewriter text animations

3. **Footer.tsx**
   - Add newsletter subscription form
   - Expand link sections
   - Add recent campaigns section
   - Implement social media feeds

4. **RandomBrush Components**
   - Create variations for borders
   - Add as section dividers
   - Implement animated versions
   - Create reusable utility classes

## Styling Strategy

### Custom Tailwind Extensions
```css
/* Add to tailwind config */
- Custom fonts: 'courier-prime', 'permanent-marker'
- Scribble border utilities
- Glitch animation classes
- Punk color palette:
  - blood-red: #8B0000
  - ink-black: #0A0A0A
  - paper-white: #FAFAFA
  - protest-yellow: #FFD700
```

### CSS Modules for Complex Effects
- `glitch.module.css` - Glitch text effects
- `scribble.module.css` - Hand-drawn borders
- `distort.module.css` - Image distortion on hover
- `typewriter.module.css` - Typewriter text animation

## Content Architecture Extensions

### New Content Collections

1. **campaigns/**
   ```yaml
   ---
   title: string
   startDate: Date
   endDate: Date
   featuredImage: string
   videoEmbed: string (optional)
   targetAmount: number (optional)
   currentAmount: number (optional)
   tags: string[]
   priority: 'urgent' | 'high' | 'normal'
   ---
   ```

2. **media/**
   ```yaml
   ---
   type: 'video' | 'gallery' | 'audio'
   title: string
   source: string | string[]
   caption: string
   tags: string[]
   ---
   ```

3. **actions/**
   ```yaml
   ---
   title: string
   type: 'petition' | 'donation' | 'event'
   targetGoal: number
   currentProgress: number
   deadline: Date
   ---
   ```

## Implementation Phases

### Phase 1: Core Visual Components (Week 1)
- [ ] HeroCampaign.tsx
- [ ] CampaignCard.tsx
- [ ] Enhance Header.tsx with hero variations

### Phase 2: Content Components (Week 2)
- [ ] MediaBlock.tsx
- [ ] Sidebar.tsx
- [ ] QuoteBlock.tsx

### Phase 3: Engagement Components (Week 3)
- [ ] CallToAction.tsx
- [ ] PetitionForm.tsx
- [ ] Enhance Footer.tsx with newsletter

### Phase 4: Polish & Animation (Week 4)
- [ ] TimelineEvent.tsx
- [ ] CSS animations and effects
- [ ] Mobile optimizations
- [ ] Performance tuning

## Design Principles

1. **Punk Aesthetic**
   - Hand-drawn elements
   - Rough edges and borders
   - High contrast colors
   - Distressed textures

2. **Activist Functionality**
   - Clear calls-to-action
   - Progress indicators
   - Social sharing
   - Time-sensitive content

3. **Performance**
   - Lazy load media
   - Optimize images
   - Minimize JavaScript
   - Progressive enhancement

4. **Accessibility**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support
   - High contrast mode

## Testing Checklist

- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Cross-browser compatibility
- [ ] Accessibility audit
- [ ] Performance metrics
- [ ] SEO optimization
- [ ] Social media previews
- [ ] Form validation
- [ ] Error handling

## Notes

- All components should support both light and dark themes
- Maintain consistent spacing using Tailwind's spacing scale
- Use TypeScript for all new components
- Follow existing code conventions in the project
- Test with real content from the current Adbusters site
- Consider progressive enhancement for JavaScript features