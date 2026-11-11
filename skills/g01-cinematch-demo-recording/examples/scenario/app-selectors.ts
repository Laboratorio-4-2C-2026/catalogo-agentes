/**
 * Everything the scenario needs to know about the app's markup, in one place.
 * Fill these in from the app's source before the first recording: the
 * scenario files never name a test id or a label themselves.
 */
export const AppSelector = {
  LOGIN_PATH: '<login route>',
  LOGIN_HEADING: '<heading shown on the login screen>',
  LOGIN_BUTTON: '<label of the login button>',
  DECK: '<test id of the deck container>',
  ACTIVE_CARD: '<test id of the active card slot>',
  CARD: '<test id of the card inside it>',
  CARD_ID_ATTRIBUTE: '<attribute that carries the card item id>',
  DETAILS_PANE: '<test id of the details pane>',
  DETAILS_PANE_EXPANDED_ATTRIBUTE: '<attribute set to "true" while the pane is expanded>',
  DETAILS_PANE_HANDLE: '<test id of the pane drag handle>',
} as const;
