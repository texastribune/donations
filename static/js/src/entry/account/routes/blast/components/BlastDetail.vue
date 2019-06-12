<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="isCancelled" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="/blastform">Renew your subscription to The Blast</a>
        </span>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link :to="{ name: 'blast-payments' }"
            >See your payment history</router-link
          >
        </span>
      </li>
    </ul>
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'BlastDetail',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isCancelled: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
