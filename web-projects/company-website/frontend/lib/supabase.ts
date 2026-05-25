import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 数据库类型定义
export interface News {
  id: string
  title: string
  slug: string
  summary: string | null
  content: string
  cover_image_url: string | null
  category: string
  tags: string[] | null
  author_id: string | null
  published_at: string | null
  is_published: boolean
  view_count: number
  created_at: string
  updated_at: string
}

export interface ContactSubmission {
  id: string
  name: string
  email: string
  phone: string | null
  company: string | null
  subject: string
  message: string
  status: 'new' | 'read' | 'replied' | 'archived'
  created_at: string
}

export interface NewsletterSubscriber {
  id: string
  email: string
  name: string | null
  is_active: boolean
  created_at: string
}
