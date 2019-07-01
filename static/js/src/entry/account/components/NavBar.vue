<template>
  <nav class="c-navbar c-navbar--light">
    <div class="c-navbar__top l-align-center-x">
      <a
        href="https://www.texastribune.org"
        class="c-navbar__logo l-align-center-self"
      >
        <img alt="The Texas Tribune" src="../svg/tt.svg" />
      </a>

      <div class="c-navbar__content">
        <ul class="c-navbar__items is-hidden-until-bp-l">
          <li
            v-if="showRouteLinks"
            class="c-navbar__item c-navbar__item--space-right"
          >
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              exact
              ga-on="click"
              :to="{ name: 'home' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.home"
            >
              <strong>Account Overview</strong>
            </router-link>
          </li>
          <li
            v-if="showMembershipLink"
            class="c-navbar__item c-navbar__item--space-right"
          >
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              ga-on="click"
              :to="{ name: 'membership' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.membership"
            >
              <strong>Membership</strong>
            </router-link>
          </li>
          <li
            v-if="showBlastLinks"
            class="c-navbar__item c-navbar__item--space-right"
          >
            <router-link
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              ga-on="click"
              :to="{ name: 'blast' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.top"
              :ga-event-label="ga.userPortalNav.labels.blast"
            >
              <strong>The Blast</strong>
            </router-link>
          </li>
          <li v-if="isLoggedIn" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              @click="logOut"
            >
              <strong>Log Out</strong>
            </button>
          </li>
          <li v-if="!isLoggedIn" class="c-navbar__item">
            <button
              class="c-navbar__item-content c-navbar__clickable c-navbar__clickable--animated t-size-xxs t-uppercase t-uppercase--extra-wide"
              active-class="is-active"
              @click="logIn"
            >
              <strong>Log In</strong>
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
        <li v-if="showRouteLinks" class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            active-class="is-active"
            exact
            ga-on="click"
            :to="{ name: 'home' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.home"
          >
            <strong>Account Overview</strong>
          </router-link>
        </li>
        <li v-if="showMembershipLink" class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'membership' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.membership"
          >
            <strong>Membership</strong>
          </router-link>
        </li>
        <li v-if="showBlastLinks" class="c-navbar__dropdown-item">
          <router-link
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            active-class="is-active"
            ga-on="click"
            :to="{ name: 'blast' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.top"
            :ga-event-label="ga.userPortalNav.labels.blast"
          >
            <strong>The Blast</strong>
          </router-link>
        </li>
        <li class="c-navbar__dropdown-item">
          <button
            class="c-navbar__clickable t-size-xxs t-uppercase t-uppercase--extra-wide"
            @click="logOut"
          >
            <strong>Log Out</strong>
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { logOut, logIn } from '../utils/auth-actions';

export default {
  name: 'NavBar',

  props: {
    showRouteLinks: {
      type: Boolean,
      required: true,
    },

    showBlastLinks: {
      type: Boolean,
      required: true,
    },

    showMembershipLink: {
      type: Boolean,
      required: true,
    },

    isLoggedIn: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      showDropdown: false,
    };
  },

  methods: {
    logOut,
    logIn,
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
  },
};
</script>
