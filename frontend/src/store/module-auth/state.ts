import { RewardsPolicy, User } from 'src/contracts'

export interface AuthStateInterface {
  user: User | null,
  rewardsPolicy: RewardsPolicy | null,
  status: 'pending' | 'success' | 'error',
  errors: { message: string, field?: string }[]
}

function state (): AuthStateInterface {
  return {
    user: null,
    rewardsPolicy: null,
    status: 'pending',
    errors: []
  }
}

export default state
