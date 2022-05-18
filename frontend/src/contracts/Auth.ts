export interface ApiToken {
    type: 'token'
    token: string
    expires_at?: string
    expires_in?: number
}

export interface RegisterData {
    email: string
    userType: string
    name: string
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
    userType: string
    name:string
    wallet: string
    algos: number
    ecoCoins: number
}

export interface RewardsPolicy {
    categoryA: number
    categoryB: number
    categoryC: number
    categoryD: number
    categoryE: number
    categoryF: number
}
