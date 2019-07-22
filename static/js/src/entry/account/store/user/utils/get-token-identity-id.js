export default function getTokenIdentityId(identities, tokenEmail) {
  const [goodIdentity] = identities.filter(({ email }) => email === tokenEmail);
  return goodIdentity.id;
}
