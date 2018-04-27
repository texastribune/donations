import Vue from 'vue';
import Vuex from 'vuex';

import FormModule from '../../store/modules/form';

Vue.use(Vuex);

export default function createStore() {
  return new Vuex.Store({
    modules: {
      baseForm: FormModule,
    },
  });
}
