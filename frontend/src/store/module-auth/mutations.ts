// autentifikačný aparát pre frontend sme použili so súhlasom Ing. Eduard Kuric, PhD.
// poskytnutého k predmetu Vývoj progresívnych webových aplikácii
// https://github.com/kurice/vpwa22/tree/main/prednasky/slek/part2

import { RewardsPolicy, User } from 'src/contracts'
import { MutationTree } from 'vuex'
import { AuthStateInterface } from './state'

const mutation: MutationTree<AuthStateInterface> = {
  AUTH_START (state) {
    state.status = 'pending'
    state.errors = []
  },
  AUTH_SUCCESS (state, { user, rewardsPolicy }: { user: User | null, rewardsPolicy: RewardsPolicy | null }) {
    state.status = 'success'
    state.user = user
    state.rewardsPolicy = rewardsPolicy
  },
  AUTH_ERROR (state, errors) {
    state.status = 'error'
    state.errors = errors
  }
}

export default mutation
