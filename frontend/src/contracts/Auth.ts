export interface ApiToken {
    type: 'token'
    token: string
    expires_at?: string
    expires_in?: number
}

export interface RegisterData {
    email: string
    userType: string
    wallet: string
    password: string
    passwordConfirmation: string
}

export interface LoginCredentials {
    email: string
    password: string
    remember: boolean
}

export interface User {
    id: number
    email: string
    wallet: string
    userType: string
    createdAt: string,
    updatedAt: string
}
