// autentifikačný aparát pre frontend sme použili so súhlasom Ing. Eduard Kuric, PhD.
// poskytnutého k predmetu Vývoj progresívnych webových aplikácii
// https://github.com/kurice/vpwa22/tree/main/prednasky/slek/part2

import { Module } from 'vuex';
import { StateInterface } from '../index';
import state, { AuthStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const authModule: Module<AuthStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default authModule;
