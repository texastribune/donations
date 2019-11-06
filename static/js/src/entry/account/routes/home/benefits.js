const BENEFITS = [
  {
    id: 0,
    component: {
      name: 'Decal',
      render(h) {
        return h('span', [
          'Our ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://twitter.com/TexasTribune/status/1058042543273848837/photo/1',
              },
            },
            'official member decal'
          ),
        ]);
      },
    },
  },
  {
    id: 1,
    component: {
      name: 'Email',
      render(h) {
        return h('span', [
          'Behind-the-scenes access to our newsroom via a monthly ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://mailchi.mp/texastribune/your-april-membersonly-newsletter-356341',
              },
            },
            'members-only newsletter'
          ),
          ' and quarterly stakeholder reports',
        ]);
      },
    },
  },
  {
    id: 2,
    component: {
      name: 'Wall',
      render(h) {
        return h('span', [
          'Our utmost gratitude and a special place on our ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://www.texastribune.org/support-us/donors-and-members/',
              },
            },
            'growing donor wall'
          ),
        ]);
      },
    },
  },
  {
    id: 3,
    component: {
      name: 'Festival',
      render(h) {
        return h('span', [
          'Informed Members also receive: Special perks at ',
          h(
            'a',
            {
              attrs: {
                href: 'https://festival.texastribune.org',
              },
            },
            'Texas Tribune Festival'
          ),
          ' our annual, three-day meeting of the brightest minds in politics and policy',
        ]);
      },
    },
  },
  {
    id: 4,
    component: {
      name: 'Engaged',
      render(h) {
        return h(
          'span',
          'Engaged Members also receive: Invites to exclusive events'
        );
      },
    },
  },
  {
    id: 5,
    component: {
      name: 'Involved',
      render(h) {
        return h('span', [
          'Involved Members also receive: Discounted ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://www.texastribune.org/studio-919/downtown-austin-event-space-congress/',
              },
            },
            'Studio 919'
          ),
          ' rental rates',
        ]);
      },
    },
  },
];

export default BENEFITS;
