// Internal normalized replacement budget. These units are assumptions, not game DPS.
const {create, C} = require('./nadia_simulator_core.js');

const DURATION = 20;
const BASE_RES = 0.10;
const NORMAL_UNIT_PER_PERCENT = 0.007;
const DIRECT_UNIT_PER_PERCENT = 0.011;
const ODETTE_PERSONAL_UNITS = 18;

function resistanceMultiplier(res) {
  return res < 0 ? 1 - res / 2 : 1 - res;
}

function scenario(name, overrides = {}) {
  return {
    name, kind: 'conduct', route: 'heavy', reactionTimes: [1, 4, 7, 10, 13, 16, 19],
    nativeUnits: 100, ordinaryUnits: 60, neutralUnits: 20,
    externalShred: 0, furnaceHolder: false, noBurst: false, missedReturn: false,
    wave: false, ...overrides
  };
}

const scenarios = [
  scenario('SSC 单体 Boss'),
  scenario('SSW 群怪', {kind: 'swirl', route: 'light', reactionTimes: [1, 3.6, 6.2, 8.8, 11.4, 14, 16.6, 19.2], nativeUnits: 150, ordinaryUnits: 45}),
  scenario('风雷混合队', {kind: 'mixed', route: 'light', reactionTimes: [1, 3.6, 6.2, 8.8, 11.4, 14, 16.6, 19.2], nativeUnits: 110, ordinaryUnits: 50}),
  scenario('已有 40% 外部减抗', {externalShred: 0.40}),
  scenario('其他角色持有炉心', {furnaceHolder: true}),
  scenario('10–13 秒换波', {wave: true}),
  scenario('不开 Q', {noBurst: true}),
  scenario('少一次完整归衡', {missedReturn: true})
];

function run(s, {personalScale = 1, odetteUptime = 1, shredEligibleShare = 1} = {}) {
  const m = create({constellation: 0, er: 180, energy: 50, artifact: !s.furnaceHolder});
  if (s.route === 'heavy') m.castSkill(true); else m.castSkill();
  m.setOnField(false);
  const baseNative = s.nativeUnits / s.reactionTimes.length;
  const baseOrdinary = s.ordinaryUnits / s.reactionTimes.length;
  const baseNeutral = s.neutralUnits / s.reactionTimes.length;
  let nadiaTeam = 0;
  let odetteTeam = 0;
  let bonusHits = 0;
  let shredHits = 0;
  let liveHits = 0;
  let burstDone = false;
  let returnDone = false;

  for (const [index, time] of s.reactionTimes.entries()) {
    m.advance(time - m.snapshot().time);
    if (s.wave) {
      const valid = !(time >= 10 && time < 13);
      if (m.snapshot().targetValid !== valid) m.setTarget(valid, valid ? 'wave-2' : 'wave-gap');
    }
    if (!s.noBurst && !burstDone && index >= 2) {
      m.setOnField(true);
      m.burst();
      m.setOnField(false);
      burstDone = true;
    }
    if (!s.noBurst && !s.missedReturn && !returnDone && index >= 4) {
      // By this point two post-Q reactions have rebuilt H to the endpoint.
      m.recastSkill();
      m.setOnField(false);
      returnDone = true;
    }
    const inRange = m.snapshot().targetValid;
    const kind = s.kind === 'mixed' ? (index % 2 ? 'conduct' : 'swirl') : s.kind;
    if (inRange) m.reaction(kind, {id: `${s.name}-${index}`, onField: false});
    const fx = m.snapshot().effects;
    const shredType = kind === 'swirl' ? 'anemo' : 'electro';
    const ext = s.externalShred;
    const shreddedRes = resistanceMultiplier(BASE_RES - ext - fx.shred[shredType] / 100);
    const odetteRes = resistanceMultiplier(BASE_RES - ext);
    const nadiaRes = shreddedRes * shredEligibleShare + odetteRes * (1 - shredEligibleShare);
    const commonBonus = s.furnaceHolder ? 0.50 : 0;
    const nadiaBonus = (fx.characterBonus + fx.artifactTeamBonus) / 100;
    const odetteBonus = 0.60 * odetteUptime + (s.furnaceHolder ? 0 : 0.50);
    const odetteBase = 1 + 0.14 * odetteUptime;
    // Both sides receive the same native and ordinary event ledger.
    nadiaTeam += baseNative * (1 + commonBonus + nadiaBonus) * nadiaRes;
    odetteTeam += baseNative * (1 + commonBonus + odetteBonus) * odetteBase * odetteRes;
    nadiaTeam += baseOrdinary * nadiaRes;
    odetteTeam += baseOrdinary * odetteRes;
    nadiaTeam += baseNeutral;
    odetteTeam += baseNeutral;
    if (fx.characterBonus) bonusHits++;
    if (fx.shred[shredType]) shredHits++;
    if (inRange) liveHits++;
  }
  m.advance(DURATION - m.snapshot().time);
  const state = m.snapshot();
  // Personal conversion is a sensitivity input: ordinary and Direct Stellar coefficients
  // cannot be added without a full character-stat and native-reaction calculation.
  let nadiaPersonal = 0;
  for (const hit of state.events.filter(e => e.kind === 'damage')) {
    const factor = hit.type === 'ordinary' ? NORMAL_UNIT_PER_PERCENT : DIRECT_UNIT_PER_PERCENT;
    const element = hit.type === 'ordinary' ? 'cryo' : hit.type === 'swirl' ? 'anemo' : 'electro';
    const routeShred = element === 'cryo' || (s.route === 'light' && element === 'anemo') ||
      (s.route === 'heavy' && element === 'electro') ? C.shred / 100 : 0;
    const resist = resistanceMultiplier(BASE_RES - s.externalShred - routeShred);
    const stellarBonus = hit.type === 'ordinary' ? 1 : 1 + (hit.characterBonus + hit.artifactBonus) / 100;
    nadiaPersonal += hit.coefficient * factor * stellarBonus * resist;
  }
  nadiaPersonal *= personalScale;
  const odettePersonal = ODETTE_PERSONAL_UNITS * personalScale * resistanceMultiplier(BASE_RES - s.externalShred);
  // Four front-field Cryo particles and one first-response background particle.
  const ownEnergy = (C.initialParticles * 3 + (liveHits ? C.firstResponseParticles * 1.8 : 0)) * 1.8;
  const requiredExternalBaseEnergy = s.noBurst ? 0 : Math.max(0, C.burstCost - ownEnergy) / 1.8;
  const nadiaFieldSeconds = 0.68 + (s.noBurst ? 0 : 1.34) + (returnDone ? 0.60 : 0);
  return {
    scenario: s.name,
    nadiaIndex: +(nadiaTeam + nadiaPersonal).toFixed(1),
    odetteIndex: +(odetteTeam + odettePersonal).toFixed(1),
    ratio: +((nadiaTeam + nadiaPersonal) / (odetteTeam + odettePersonal)).toFixed(3),
    nadiaPersonal: +nadiaPersonal.toFixed(1),
    odettePersonal: +odettePersonal.toFixed(1),
    bonusCoverage: `${bonusHits}/${s.reactionTimes.length}`,
    routeShredCoverage: `${shredHits}/${s.reactionTimes.length}`,
    targetCoverage: `${liveHits}/${s.reactionTimes.length}`,
    nadiaFieldSeconds: +nadiaFieldSeconds.toFixed(2),
    odetteFieldSeconds: 1.5,
    requiredExternalBaseEnergy: +requiredExternalBaseEnergy.toFixed(1),
    survivalSlot: '均需队友承担',
    coefficients: state.coefficients,
    metrics: state.metrics
  };
}

function main() {
  const rows = scenarios.map(s => run(s));
  console.table(rows.map(({scenario, nadiaIndex, odetteIndex, ratio, nadiaPersonal,
    bonusCoverage, routeShredCoverage, nadiaFieldSeconds, requiredExternalBaseEnergy}) =>
    ({scenario, nadiaIndex, odetteIndex, ratio, nadiaPersonal, bonusCoverage,
      routeShredCoverage, nadiaFieldSeconds, requiredExternalBaseEnergy})));
  const sensitivity = [];
  for (const shredEligibleShare of [0.5, 1]) for (const odetteUptime of [0.75, 1]) {
    const ratios = scenarios.map(s => run(s, {shredEligibleShare, odetteUptime}).ratio);
    sensitivity.push({shredEligibleShare, odetteUptime,
      scenariosOverTenPercent: ratios.filter(x => x > 1.10).length,
      minRatio: Math.min(...ratios), maxRatio: Math.max(...ratios)});
  }
  console.table(sensitivity);
  if (process.argv.includes('--json')) console.log(JSON.stringify({assumptions: {duration: DURATION,
    ordinaryUnitPerPercent: NORMAL_UNIT_PER_PERCENT, directUnitPerPercent: DIRECT_UNIT_PER_PERCENT,
    odettePersonalUnits: ODETTE_PERSONAL_UNITS}, rows, sensitivity}, null, 2));
}

if (require.main === module) main();
module.exports = {run, scenarios, resistanceMultiplier};
