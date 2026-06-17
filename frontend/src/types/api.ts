export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  perPage: number
  pages: number
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar_url: string | null
  role: 'user' | 'admin'
  created_at: string
}

export interface CommunityPost {
  id: number
  user_id: number
  username: string
  user_avatar: string | null
  title: string
  content: string
  images: string[]
  recipe_id: number | null
  view_count: number
  like_count: number
  comment_count: number
  is_liked: boolean
  is_pinned: boolean
  status: string
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  post_id: number
  user_id: number
  username: string
  user_avatar: string | null
  parent_id: number | null
  content: string
  created_at: string
  replies?: Comment[]
}

export interface Category {
  id: number
  name: string
  description: string
  sort_order: number
}

export interface RatingInfo {
  avgRating: number
  ratingCount: number
  userScore: number | null
}

export interface AdminStats {
  total_users: number
  total_recipes: number
  total_posts: number
  total_comments: number
  pending_recipes: number
  flagged_posts: number
}
