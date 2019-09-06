/* eslint-disable no-param-reassign, camelcase */

import parse from 'date-fns/parse';
import isPast from 'date-fns/is_past';

export default function addFields(data) {
  const {
    is_recurring_donor,
    membership_expiration_date,
    membership_level,
    never_given,
    next_transaction,
    is_mdev,
    is_current_circle,
    is_former_circle,
    is_current_blast_subscriber,
    is_former_blast_subscriber,
  } = data;
  let membershipLevel;
  let isExpired;
  let willExpire;

  const isBlastSubscriber =
    is_current_blast_subscriber || is_former_blast_subscriber;

  const isSingleDonor =
    !never_given &&
    !is_recurring_donor &&
    !!membership_expiration_date &&
    !is_mdev;

  const isRecurringDonor =
    is_recurring_donor &&
    !!membership_expiration_date &&
    !is_mdev &&
    !is_current_circle &&
    !is_former_circle;

  const isCircleDonor =
    (is_current_circle || is_former_circle) && !!membership_expiration_date;

  const isCustomDonor =
    (is_mdev && !is_current_circle && !is_former_circle) ||
    (!never_given && !membership_expiration_date);

  if (membership_expiration_date) {
    isExpired = isPast(parse(membership_expiration_date));
    willExpire = !next_transaction && !isExpired;
  } else {
    isExpired = null;
    willExpire = null;
  }

  if (membership_level) {
    membershipLevel = membership_level.toLowerCase();
  } else {
    membershipLevel = null;
  }

  delete data.is_mdev;
  delete data.is_former_circle;
  delete data.is_current_circle;

  // The following booleans are mutually exclusive:
  // is_single_donor, is_recurring_donor, is_circle_donor, is_custom_donor
  // the first three are guaranteed to have a string expiration date
  // all are guaranteed to have never_given: false

  return {
    ...data,
    is_single_donor: isSingleDonor,
    is_recurring_donor: isRecurringDonor,
    is_circle_donor: isCircleDonor,
    is_custom_donor: isCustomDonor,
    is_expired: isExpired,
    is_blast_subscriber: isBlastSubscriber,
    will_expire: willExpire,
    membership_level: membershipLevel,
  };
}
