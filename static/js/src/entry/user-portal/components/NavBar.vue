<template>
  <nav class="c-navbar c-navbar--standard c-navbar--light">
    <div class="c-navbar__top l-align-center-x">
      <a
        href="https://www.texastribune.org"
        class="c-navbar__logo l-align-center-self"
      >
        <img alt="The Texas Tribune" src="../svg/tt.svg" />
      </a>

      <div class="c-navbar__content">
        <ul class="c-navbar__items is-hidden-until-bp-l">
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              exact
              :to="{ name: 'home' }"
              ><strong>Account Overview</strong></router-link
            >
          </li>
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              :to="{ name: 'membership' }"
              ><strong>Membership</strong></router-link
            >
          </li>
          <li class="c-navbar__item c-navbar__item--space-right">
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              :to="{ name: 'blast' }"
              ><strong>The Blast</strong></router-link
            >
          </li>
          <li class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              @click="user.logOut"
            >
              <strong>Log Out</strong>
            </button>
          </li>
        </ul>

        <ul class="c-navbar__items is-hidden-from-bp-l">
          <li v-if="!showDropdown" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
              aria-label="Show menu"
              @click="toggleDropdown"
            >
              <icon name="bars" :display="{ size: 's' }" />
              <strong>&nbsp;Menu</strong>
            </button>
          </li>
          <li v-else class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
              aria-label="Hide menu"
              @click="toggleDropdown"
            >
              <icon name="close" :display="{ size: 's' }" />
              <strong>&nbsp;Close</strong>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="showDropdown" class="c-navbar__dropdown is-hidden-from-bp-l">
      <ul class="c-navbar__dropdown-items">
        <li class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            :to="{ name: 'home' }"
            active-class="is-active"
            exact
            ><strong>Account Overview</strong></router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            :to="{ name: 'membership' }"
            active-class="is-active"
            ><strong>Membership</strong></router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            :to="{ name: 'blast' }"
            active-class="is-active"
            ><strong>The Blast</strong></router-link
          >
        </li>
        <li class="c-navbar__dropdown-item">
          <button
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            @click="user.logOut"
          >
            <strong>Log Out</strong>
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import userMixin from '../mixins/user';

export default {
  name: 'NavBar',

  mixins: [userMixin],

  data() {
    return {
      showDropdown: false,
    };
  },

  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>
