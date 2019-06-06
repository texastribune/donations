<template>
  <nav class="c-side-nav">
    <ul class="c-side-nav__outer t-size-s">
      <li class="has-xxs-btm-marg">
        <router-link
          :to="{ name: 'home' }"
          exact
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ><strong>Account Overview</strong></router-link
        >
      </li>
      <li v-if="!user.never_given" class="has-xxs-btm-marg">
        <router-link
          :to="{ name: 'membership' }"
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ><strong>Membership</strong></router-link
        >
        <ul class="c-side-nav__inner">
          <li>
            <router-link
              :to="{ name: 'payments' }"
              class="has-text-gray-dark has-text-hover-gray"
              active-class="is-active"
              >Donation History</router-link
            >
          </li>
        </ul>
      </li>
      <li v-if="user.is_blast_member" class="has-xxs-btm-marg">
        <router-link
          :to="{ name: 'blast' }"
          class="has-text-black-off has-text-hover-gray"
          active-class="is-active"
          ><strong>The Blast Newsletter</strong></router-link
        >
        <ul class="c-side-nav__inner">
          <li class="c-side-nav__item c-side-nav__item--inside">
            <router-link
              :to="{ name: 'blast-payments' }"
              class="has-text-gray-dark has-text-hover-gray"
              active-class="is-active"
              >Payment History</router-link
            >
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'SideNav',

  props: {
    user: {
      type: Object,
      required: true,
    },
  },
};
</script>
