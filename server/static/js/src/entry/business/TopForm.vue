<template>
  <form
    ref="form"
    action="/business"
    method="post"
    class="form business-form"
    @submit="$event.preventDefault()"
  >
    <div v-show="serverErrorMessage" class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col">
          <p class="form__error form__error--prominent">
            {{ serverErrorMessage }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col">
          <form-buckets :all-levels="allLevels" :store-module="storeModule" />
        </div>
      </div>
    </div>

    <div class="grid_container--m">
      <benefits />
      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="email address"
            type="email"
            base-classes="form__text form__text--standard"
            name="stripeEmail"
            inputmode="email"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="organization name"
            base-classes="form__text form__text--standard"
            name="business_name"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="website"
            base-classes="form__text form__text--standard"
            name="website"
            inputmode="url"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="street address"
            base-classes="form__text form__text--standard"
            name="shipping_street"
          />
        </div>
      </div>

      <div class="grid_row grid_separator grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="city"
            base-classes="form__text form__text--standard"
            name="shipping_city"
          />
        </div>
        <div class="col_4 grid_separator">
          <select-list
            :options="usStatesOptions"
            :store-module="storeModule"
            label-text="state"
            base-classes="form__text form__text--standard"
            name="shipping_state"
          />
        </div>
        <div class="col_2 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="zip code"
            base-classes="form__text form__text--standard"
            name="shipping_postalcode"
            inputmode="numeric"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="contact first name"
            base-classes="form__text form__text--standard"
            name="first_name"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="contact last name"
            base-classes="form__text form__text--standard"
            name="last_name"
          />
        </div>
      </div>

      <div class="grid_row grid_separator grid_wrap--s">
        <div class="col grid_separator">
          <text-input
            :required="false"
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="I am giving because"
            base-classes="form__text form__text--standard"
            name="reason"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <pay-fees :store-module="storeModule" base-classes="form__fees" />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <native-pay
            :store-module="storeModule"
            :form-is-valid="isValid"
            :supported="nativeIsSupported"
            base-classes="form__native"
            @setLocalValue="setLocalValue"
            @setCardValue="setCardValue"
            @onSubmit="onSubmit"
          />
        </div>
      </div>

      <div
        v-if="nativeIsSupported && showManualPay"
        class="grid_separator--l"
        aria-hidden="true"
      />

      <div
        :aria-live="nativeIsSupported ? 'polite' : false"
        class="grid_separator"
      >
        <div v-if="showManualPay">
          <div class="grid_row">
            <div class="col">
              <manual-pay
                :card="card"
                base-classes="form__manual"
                @setCardValue="setCardValue"
              />
            </div>
          </div>

          <div class="grid_row grid_separator">
            <div class="col">
              <manual-submit
                :form-is-valid="isValid && card.isValid"
                :is-fetching-token="isFetchingToken"
                base-classes="form__submit button button--yellow button--l"
                value="Donate"
                @setLocalValue="setLocalValue"
                @setCardValue="setCardValue"
                @onSubmit="onSubmit"
              />
            </div>
          </div>
        </div>

        <p class="subtext">
          The Texas Tribune is a 501(c)(3), and your organization's gift is tax
          deductible
        </p>
      </div>

      <div v-if="genericErrorMessage" class="grid_separator">
        <div class="grid_row">
          <div class="col">
            <p
              role="alert"
              class="form__error form__error--normal form__error--centered"
            >
              {{ genericErrorMessage }}
            </p>
          </div>
        </div>
      </div>

      <p class="subtext">
        This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy">Privacy Policy</a> and
        <a href="https://policies.google.com/terms">Terms of Service</a> apply.
      </p>

      <local-hidden :value="stripeToken" name="stripeToken" />
      <local-hidden :value="recaptchaToken" name="recaptchaToken" />
      <hidden name="campaign_id" :store-module="storeModule" />
      <hidden name="referral_id" :store-module="storeModule" />
      <hidden name="description" :store-module="storeModule" />
      <hidden name="pay_fees_value" :store-module="storeModule" />
      <hidden name="installment_period" :store-module="storeModule" />
      <hidden name="amount" :store-module="storeModule" />
      <hidden name="level" :store-module="storeModule" />
    </div>
  </form>
</template>

<script>
import Hidden from '../../connected-elements/Hidden.vue';
import PayFees from '../../connected-elements/PayFees.vue';
import TextInput from '../../connected-elements/TextInput.vue';
import SelectList from '../../connected-elements/SelectList.vue';
import FormBuckets from '../../connected-elements/FormBuckets.vue';
import ManualPay from '../../payment-elements/ManualPay.vue';
import ManualSubmit from '../../payment-elements/ManualSubmit.vue';
import NativePay from '../../payment-elements/NativePay.vue';
import LocalHidden from '../../local-elements/Hidden.vue';
import Benefits from './Benefits.vue';
import formStarter from '../../mixins/connected-form/starter';
import { US_STATES_SELECT_LIST, BUSINESS_LEVELS } from './constants';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    SelectList,
    PayFees,
    ManualPay,
    ManualSubmit,
    NativePay,
    FormBuckets,
    Benefits,
  },

  mixins: [formStarter],

  data() {
    return {
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      usStatesOptions: US_STATES_SELECT_LIST,
      storeModule: 'businessForm',
      allLevels: BUSINESS_LEVELS,
    };
  },
};
</script>
