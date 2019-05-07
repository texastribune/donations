<template>
  <div>
    <message :name="welcomeMessageKey"> <p>Welcome message.</p> </message>
    <message :name="comingSoonMessageKey">
      <p>Coming soon message.</p>
    </message>
    <ul>
      <li v-for="datum in data" :key="datum.id">{{ datum.headline }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import Message from './components/Message.vue';
import { WELCOME_MESSAGE_KEY, COMING_SOON_MESSAGE_KEY } from '../../constants';

export default {
  name: 'Index',

  components: { Message },

  mixins: [routeMixin, routeFetchMixin],

  data() {
    return {
      data: [],
      welcomeMessageKey: WELCOME_MESSAGE_KEY,
      comingSoonMessageKey: COMING_SOON_MESSAGE_KEY,
    };
  },

  methods: {
    async fetchData() {
      const {
        data: { results },
      } = await axios.get('https://www.texastribune.org/api/v2/content/');

      this.data = results;
    },
  },
};
</script>
