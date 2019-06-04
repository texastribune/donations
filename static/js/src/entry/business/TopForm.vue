<template>
  <form
    ref="form"
    action="/business"
    method="post"
    class="form business-form"
    @submit="$event.preventDefault()"
  >
    <div
      v-show="showServerErrorMessage"
      class="grid_container--l grid_separator"
    >
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
            label-text="encouraged to give by"
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
            @onSubmit="onSubmit"
          />
        </div>
      </div>

      <div
        v-if="nativeIsSupported && showManualPay"
        class="grid_separator--l"
        aria-hidden="true"
      />

      <div :aria-live="nativeIsSupported ? 'polite' : false">
        <div v-if="showManualPay">
          <div class="grid_row">
            <div class="col">
              <manual-pay
                :show-error="showErrors && showCardError"
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

      <div v-if="showErrorClue" class="grid_separator--l" aria-hidden="true" />

      <div v-if="showErrorClue" class="grid_row" aria-hidden="true">
        <div class="col">
          <p class="form__error form__error--normal form__error--centered">
            Please correct errors above
          </p>
        </div>
      </div>

      <local-hidden :value="stripeToken" name="stripeToken" />
      <hidden name="campaign_id" :store-module="storeModule" />
      <hidden name="referral_id" :store-module="storeModule" />
      <hidden name="description" :store-module="storeModule" />
      <hidden name="pay_fees_value" :store-module="storeModule" />
      <hidden name="installment_period" :store-module="storeModule" />
      <hidden name="amount" :store-module="storeModule" />
    </div>
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import LocalHidden from '../../elements/LocalHidden.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import SelectList from '../../elements/SelectList.vue';
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import FormBuckets from '../../elements/FormBuckets.vue';
import Benefits from './Benefits.vue';
import formStarter from '../../mixins/form/starter';
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
