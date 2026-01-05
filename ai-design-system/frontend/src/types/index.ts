export interface ClassificationResult {
  predicted_class: 'Traditional' | 'Fusion' | 'Modern';
  confidence: number;
  probabilities: {
    Traditional: number;
    Fusion: number;
    Modern: number;
  };
}

export interface Design {
  id: string;
  filename: string;
  craft_type: string;
  style: string;
  fusion_level: number;
  prompt: string;
}

export interface User {
  user_id: number;
  user_type: string;
  age_group: string;
  gender: string;
  country: string;
  timestamp: string;
}

export interface Interaction {
  interaction_id: number;
  user_id: number;
  design_id: string;
  design_style: string;
  fusion_level: number;
  action: 'like' | 'save' | 'comment' | 'skip';
  comment_text?: string;
  timestamp: string;
}

export interface Analytics {
  total_interactions: number;
  total_users: number;
  total_likes: number;
  likes_by_style: Record<string, number>;
  user_types: Record<string, number>;
  popular_fusion_levels: Record<number, number>;
}



