/**
 * Every number shown in the deck lives here, with its source and cut date.
 * Never type a number inside a slide. Values come from the project-management
 * skill (skills/project-management.md) and the team's spreadsheet.
 */

export const cut = {
  date: '15/10/2026',
  source: 'Zest - Steering 2 (planilla 10B, línea base v2)',
};

export const evm = {
  bac: 7256,
  pv: 4493,
  ev: 6124,
  ac: 4591,
};

export const indices = {
  spi: evm.ev / evm.pv,
  cpi: evm.ev / evm.ac,
};

/**
 * EXAMPLE series to show the S-curve layout. Replace with the cumulative
 * PV/EV/AC per period from the spreadsheet, then set `isExample` to false.
 */
export const curve = {
  isExample: true,
  cutIndex: 10,
  points: [
    { label: '06/08', pv: 450, ev: 450, ac: 300 },
    { label: '13/08', pv: 900, ev: 700, ac: 650 },
    { label: '20/08', pv: 1350, ev: 1150, ac: 1050 },
    { label: '27/08', pv: 1800, ev: 1700, ac: 1500 },
    { label: '03/09', pv: 2250, ev: 2400, ac: 1950 },
    { label: '10/09', pv: 2700, ev: 3100, ac: 2400 },
    { label: '17/09', pv: 3050, ev: 3700, ac: 2850 },
    { label: '24/09', pv: 3400, ev: 4300, ac: 3300 },
    { label: '01/10', pv: 3750, ev: 4900, ac: 3750 },
    { label: '08/10', pv: 4100, ev: 5500, ac: 4150 },
    { label: '15/10', pv: 4493, ev: 6124, ac: 4591 },
    { label: '22/10', pv: 4950 },
    { label: '29/10', pv: 5450 },
    { label: '05/11', pv: 6000 },
    { label: '12/11', pv: 6600 },
    { label: '23/11', pv: 7256 },
  ],
};
