import { post, get as httpGet, put as httpPut } from './client'
import type { LoginRequest, RegisterRequest, AuthTokens, UserInfo } from '@/types/api'

export const authApi = {
  login: (data: LoginRequest) => post<AuthTokens>('/auth/login', data),
  register: (data: RegisterRequest) => post<AuthTokens>('/auth/register', data),
  refresh: (refreshToken: string) => post<AuthTokens>('/auth/refresh', { refresh_token: refreshToken }),
  logout: () => post<null>('/auth/logout'),
  getMe: () => httpGet<UserInfo>('/auth/me'),
  updateMe: (data: Partial<UserInfo>) => httpPut<UserInfo>('/auth/me', data),
  changePassword: (oldPwd: string, newPwd: string) =>
    httpPut<null>('/auth/me/password', { old_password: oldPwd, new_password: newPwd }),
}
