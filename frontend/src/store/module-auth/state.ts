import { User } from 'src/contracts'
import MyAlgoConnect from '@randlabs/myalgo-connect'

export interface AuthStateInterface {
  user: User | null,
  status: 'pending' | 'success' | 'error',
  myAlgoConnect: MyAlgoConnect | null,
  errors: { message: string, field?: string }[]
}

function state (): AuthStateInterface {
  return {
    user: null,
    status: 'pending',
    myAlgoConnect: null,
    errors: []
  }
}

export default state
