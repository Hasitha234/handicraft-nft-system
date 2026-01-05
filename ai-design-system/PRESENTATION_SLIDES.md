# Presentation Slides Content for AI Component

## SLIDE 1: Problem Definition

**Title:** 
```
Problem Definition
```

**Main Text:**
```
Sri Lankan handicraft artisans struggle to understand market preferences and create designs that appeal to both traditional and modern consumers. The industry lacks data-driven insights into which fusion designs sell best, making it difficult to balance cultural authenticity with contemporary appeal. Without AI assistance, artisans rely on intuition, leading to low market penetration and reduced competitiveness against mass-produced alternatives.
```

**Visual Elements:**
- Traditional Sri Lankan handicraft (mask/batik)
- Modern/fusion design example
- Data visualization showing market gap

---

## SLIDE 2: User Requirements Addressed

**Title:**
```
User Requirements
Addressed
```

**Left Column:**
- Handicraft Image Classification (Traditional/Fusion/Modern)
- AI-Powered Design Generation
- Controllable Fusion Level (0-100%)
- Multiple Design Variations (5+ per request)
- User Preference Collection System
- Demographic-Based Analytics
- Natural Interaction Interface (No Forced Surveys)
- Real-Time Design Feedback

**Right Column:**
- RESTful API for Integration
- Model Accuracy Tracking (79.25%)
- Exportable Data for Analysis
- Instagram-Style Gallery Interface
- Automated Preference Tracking
- Market Insights Dashboard

---

## SLIDE 3: Technical Contribution

**Title:**
```
Technical
Contribution
```

**Content:**

1. **Transfer Learning Classification System:** Fine-tuned ResNet50 on 258 Sri Lankan handicraft images achieving 79.25% accuracy for Traditional/Fusion/Modern classification.

2. **Controllable AI Design Generation:** Stable Diffusion pipeline with fusion-level control (0-100%) enabling artisans to generate designs balancing traditional authenticity with modern appeal.

3. **Natural Preference Collection:** Instagram-style interface that collects user preferences through likes, saves, and comments without forced surveys, improving data quality and user engagement.

4. **Unified API Architecture:** FastAPI server integrating all three components (classification, generation, preferences) with RESTful endpoints for seamless team integration.

5. **Data-Driven Market Insights:** SQLite-based analytics system tracking user demographics, style preferences, and fusion level popularity to guide artisan design decisions.

---

## SLIDE 4: User Feedbacks on Prototypes

**Title:**
```
User Feedbacks on
Prototypes
```

**Good User Experience:**
- Intuitive image classification with confidence scores
- Easy-to-use design generator with fusion level control
- Engaging Instagram-style preference collection
- Clear analytics dashboard for market insights
- Fast API integration for team components

**Needs Improvement:**
- Expand dataset for higher classification accuracy (>85%)
- Optimize Stable Diffusion inference speed
- Enhance prompt engineering for design precision
- Improve mobile responsiveness for preference system
- Add batch classification for multiple images

---

## Additional Slide: System Architecture

**Title:**
```
System
Architecture
```

**Three Core Components:**

1. **Component 1: Classification System**
   - ResNet50 Transfer Learning
   - 79.25% Accuracy
   - Real-time inference

2. **Component 2: Design Generator**
   - Stable Diffusion v1.5
   - Controllable Fusion (0-100%)
   - 5+ variations per request

3. **Component 3: User Preference System**
   - SQLite Database
   - Instagram-style UI
   - Analytics Dashboard

**Integration:**
- FastAPI Unified Server
- RESTful Endpoints
- Team Component Integration Ready

---

## Additional Slide: Results & Metrics

**Title:**
```
Results &
Metrics
```

**Model Performance:**
- Classification Accuracy: 79.25%
- Training Time: 12.56 minutes (20 epochs)
- Dataset: 258 images (80/20 split)

**Design Generation:**
- Designs Generated: 85+
- Craft Types: 4 (Mask, Batik, Wood Carving, Pottery)
- Fusion Levels: 0-100% (10% increments)

**System Status:**
- All 3 Components: Operational
- API Server: Ready
- Integration Tests: Passing
- Production Tools: Complete

---

## Footer Template (All Slides)

**Bottom Left:**
```
SLIIT
FACULTY OF COMPUTING
```

**Bottom Center:**
```
[YOUR_REGISTRATION_NO] | [YOUR_NAME] | [BATCH]
```

**Bottom Right:**
```
[PRESENTATION_DATE]
```





