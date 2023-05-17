<template>
  <div>
    <user-nav-bar />

    <main class="has-bg-white-off">
      <div class="l-ump-container l-align-center-x">
        <div class="l-ump-grid">
          <div class="l-ump-grid__side is-hidden-until-bp-l">
            <user-side-nav />
          </div>
          <div class="l-ump-grid__content has-bg-white"><router-view /></div>
        </div>
      </div>
    </main>

    <user-site-footer />

    <view-as-form />
  </div>
</template>

<script>
import routeMixin from '../mixin';

import userMixin from '../../store/user/mixin';

import UserSideNav from '../../nav/components/UserSideNav.vue';

const ViewAsForm = () =>
  import(/* webpackChunkName: "view-as-form" */ '../../view-as/containers/ViewAsFormContainer.vue');

export default {
  name: 'Account',

  components: { UserSideNav, ViewAsForm },

  mixins: [routeMixin, userMixin],
};
</script>
