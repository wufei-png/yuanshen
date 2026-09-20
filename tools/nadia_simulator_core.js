/* Original-character rule model. Native reactions are inputs, never inferred. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NadiaRules = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, () => {
  'use strict';
  const C = Object.freeze({
    patrol: 22, skillCooldown: 18, firstTick: 1.5, tick: 2, zeroTick: 1.5,
    zero: 12, routeCooldown: 2.5, recastCooldown: 6, returnCooldown: 4,
    switchCooldown: 1, calibration: 8, burstCooldown: 15, burstCost: 50,
    baseBonus: 40, growthPerStep: 5, calibrationBonus: 20, shred: 30,
    poiseDamageTakenReduction: 50, initialParticles: 4, firstResponseParticles: 1,
    activeIcdSeconds: 2.5, activeIcdHits: 3,
    companion: .55, c6Companion: .75, c2Elevation: 15, c6Elevation: 25,
    c4Refund: 8, weaponSelf: 24, weaponTeam: 12, weaponWindow: 20,
    weaponTeamDuration: 8, artifactDuration: 12, artifactBonus: 50,
    erDamagePerPoint: .25, erDamageCap: 30,
    e1: Object.freeze({ initial: 68, tick: 42, light: 47, heavy: 61, normal: 101, full: 128 }),
    e6: Object.freeze({ initial: 86, tick: 53, light: 60, heavy: 77, normal: 128, full: 162 }),
    e10: Object.freeze({ initial: 101, tick: 62, light: 70, heavy: 90, normal: 150, full: 190 }),
    e13: Object.freeze({ initial: 114, tick: 70, light: 79, heavy: 101, normal: 169, full: 214 }),
    q1: 242, q6: 306, q10: 360, q13: 405
  });
  const EPS = 1e-8;
  function create(options = {}) {
    const config = { constellation: 0, er: 180, energy: 50, weapon: false, artifact: false, ...options };
    if (!Number.isInteger(config.constellation) || config.constellation < 0 || config.constellation > 6) throw new Error('命座须为0至6');
    if (!Number.isFinite(config.er) || config.er < 100) throw new Error('充能须至少100%');
    if (!Number.isFinite(config.energy) || config.energy < 0 || config.energy > C.burstCost) throw new Error('初始能量须为0至50');
    const talent = config.constellation >= 3 ? C.e13 : C.e10;
    let sequence = 0;
    const seen = new Set();
    const icd = new Map();
    const s = {
      time: 0, mode: 'light', h: 0, growth: 0, patrolUntil: 0, zeroUntil: 0,
      calibrationUntil: 0, weaponUntil: 0, weaponTeamUntil: 0, artifactUntil: 0,
      nextTick: Infinity, lastSkill: -Infinity, lastRoute: -Infinity,
      lastReturn: -Infinity, lastRecast: -Infinity, lastSwitch: -Infinity, lastBurst: -Infinity,
      firstResponse: true, energy: config.energy, onField: true, targetValid: true, targetId: 'enemy-1',
      coefficients: { ordinary: 0, swirl: 0, conduct: 0 },
      metrics: { ticks: 0, skipped: 0, main: 0, companion: 0, normal: 0, full: 0,
        particles: 0, applications: 0, icdBlocked: 0, rejected: 0, duplicates: 0,
        gcdBlocked: 0, refund: 0, wastedEnergy: 0, patrolSeconds: 0,
        calibrationSeconds: 0, shredSeconds: 0, cryoShredSeconds: 0,
        anemoShredSeconds: 0, electroShredSeconds: 0, bonusIntegral: 0 },
      events: []
    };
    const patrol = () => s.time < s.patrolUntil;
    const zero = () => patrol() && s.time < s.zeroUntil;
    const calibrated = () => patrol() && s.time < s.calibrationUntil;
    const ready = (last, delay) => s.time + EPS >= last + delay;
    function log(text, kind = 'state', details = {}) { s.events.push({ time: s.time, kind, text, ...details }); }
    function reject(text) { s.metrics.rejected++; log(text, 'rejected'); return false; }
    function effects() {
      const active = patrol();
      return {
        characterBonus: active ? C.baseBonus + s.growth * C.growthPerStep + (calibrated() ? C.calibrationBonus : 0) : 0,
        elevation: active ? (config.constellation >= 6 ? C.c6Elevation : config.constellation >= 2 ? C.c2Elevation : 0) : 0,
        shred: active && s.targetValid ? (config.constellation >= 6 ? { cryo: C.shred, anemo: C.shred, electro: C.shred } :
          { cryo: C.shred, anemo: s.mode === 'light' ? C.shred : 0, electro: s.mode === 'heavy' ? C.shred : 0 }) : { cryo: 0, anemo: 0, electro: 0 },
        poiseDamageTakenReduction: calibrated() ? C.poiseDamageTakenReduction : 0,
        weaponTeamBonus: config.weapon && s.time < s.weaponTeamUntil ? C.weaponTeam : 0,
        artifactTeamBonus: config.artifact && s.time < s.artifactUntil ? C.artifactBonus : 0,
        personalErBonus: Math.min(C.erDamageCap, (config.er - 100) * C.erDamagePerPoint)
      };
    }
    function addEnergy(amount, reason) {
      if (!Number.isFinite(amount) || amount < 0) throw new Error('能量输入须非负');
      const gain = Math.min(C.burstCost - s.energy, amount);
      s.energy += gain;
      s.metrics.wastedEnergy += amount - gain;
      log(`${reason}：获得${gain.toFixed(2)}能量，溢出${(amount - gain).toFixed(2)}`, 'energy');
    }
    function particles(count) {
      s.metrics.particles += count;
      addEnergy(count * (s.onField ? 3 : 1.8) * config.er / 100, `自产${count}冰微粒，${s.onField ? '前台' : '后台'}接取假设`);
    }
    function artifactTrigger() { if (config.artifact) s.artifactUntil = s.time + C.artifactDuration; }
    function damage(type, coefficient, label) {
      if (!s.targetValid) { log(`${label}未命中`, 'miss'); return false; }
      const before = effects();
      s.coefficients[type] += coefficient;
      log(`${label}：${coefficient.toFixed(2)}%攻击力系数 / ${type}`, 'damage', {
        type, coefficient, characterBonus: before.characterBonus, elevation: before.elevation,
        weaponSelfBonus: config.weapon && !s.onField && s.time < s.weaponUntil ? C.weaponSelf : 0,
        weaponTeamBonus: before.weaponTeamBonus, artifactBonus: before.artifactTeamBonus,
        personalErBonus: before.personalErBonus
      });
      // Equipment activates after its triggering damage, never retroactively.
      if (type !== 'ordinary') artifactTrigger();
      if (config.weapon && !s.onField && s.time < s.weaponUntil) s.weaponTeamUntil = s.time + C.weaponTeamDuration;
      return true;
    }
    function apply(label, group = 'independent') {
      if (!s.targetValid) return;
      if (group === 'active') {
        const prior = icd.get(s.targetId);
        if (!prior || s.time + EPS >= prior.timer + C.activeIcdSeconds) {
          icd.set(s.targetId, { timer: s.time, hits: 0 });
        } else {
          prior.hits++;
          if (prior.hits < C.activeIcdHits) { s.metrics.icdBlocked++; log(`${label}：主动组附着被ICD抑制`, 'icd'); return; }
          prior.hits = 0; // Hit-rule applications do not restart the timer.
        }
      }
      s.metrics.applications++;
      log(`${label}：1U冰 / ${group}；是否产生原生反应须另行输入`, 'application', { targetId: s.targetId, group });
    }
    function tick(label = '自动刻度') {
      if (!s.targetValid) { s.metrics.skipped++; log(`${label}跳过，不暂停或补发`, 'miss'); return; }
      s.metrics.ticks++;
      damage('ordinary', talent.tick, label);
      apply(label);
    }
    function expire() {
      if (s.patrolUntil && !patrol()) {
        s.patrolUntil = 0; s.zeroUntil = 0; s.calibrationUntil = 0;
        s.h = 0; s.growth = 0; s.nextTick = Infinity;
        log('巡衡结束，H、成长、校准与测区清除');
      }
      if (s.zeroUntil && s.time >= s.zeroUntil) { s.zeroUntil = 0; log('测区结束；保留已排定刻度'); }
    }
    function advance(seconds) {
      if (!Number.isFinite(seconds) || seconds < 0) throw new Error('时间增量须非负有限值');
      const end = s.time + seconds;
      while (s.time < end) {
        const deadlines = [end, s.nextTick, s.patrolUntil, s.zeroUntil, s.calibrationUntil,
          s.weaponUntil, s.weaponTeamUntil, s.artifactUntil].filter(t => t > s.time);
        const next = Math.min(...deadlines);
        const dt = next - s.time;
        const fx = effects();
        if (patrol()) s.metrics.patrolSeconds += dt;
        if (calibrated()) s.metrics.calibrationSeconds += dt;
        if (fx.shred.cryo) { s.metrics.shredSeconds += dt; s.metrics.cryoShredSeconds += dt; }
        if (fx.shred.anemo) s.metrics.anemoShredSeconds += dt;
        if (fx.shred.electro) s.metrics.electroShredSeconds += dt;
        s.metrics.bonusIntegral += dt * fx.characterBonus;
        s.time = next;
        expire();
        if (patrol() && s.time === s.nextTick) {
          tick(); s.nextTick = s.time + (zero() ? C.zeroTick : C.tick);
        }
      }
      return snapshot();
    }
    function switchMode() {
      if (!ready(s.lastSwitch, C.switchCooldown)) return reject('切路尚在1秒间隔内');
      s.lastSwitch = s.time;
      s.mode = s.mode === 'light' ? 'heavy' : 'light'; s.h = 0;
      log(`选择${s.mode === 'light' ? '轻端' : '重端'}；H归零，不发归衡奖励，成长保留`);
      return true;
    }
    function returnZero(label) {
      const before = s.h; s.h = 0;
      if (!before) return false;
      if (!ready(s.lastReturn, C.returnCooldown)) return reject('归零成功；归衡奖励仍在4秒间隔内');
      s.lastReturn = s.time;
      const full = Math.abs(before) === 2;
      s.metrics[full ? 'full' : 'normal']++;
      damage('ordinary', full ? talent.full : talent.normal, `${label}${full ? '完整' : '普通'}归衡`);
      apply('归衡', 'active');
      if (full) s.calibrationUntil = s.time + C.calibration;
      log(`${full ? '完整' : '普通'}归衡：成长${s.growth}档保留${full ? '，校准8秒' : ''}`);
      return true;
    }
    function recastSkill() {
      if (!patrol()) return reject('无巡衡，不能校读');
      if (!ready(s.lastRecast, C.recastCooldown)) return reject('校读仍在6秒间隔内');
      s.onField = true; s.lastRecast = s.time;
      if (!s.h) tick('零位校读刻度'); else returnZero('E');
      return true;
    }
    function castSkill(hold = false) {
      s.onField = true;
      if (hold && !switchMode()) return false;
      if (ready(s.lastSkill, C.skillCooldown)) {
        s.lastSkill = s.time; s.patrolUntil = s.time + C.patrol;
        s.nextTick = s.time + C.firstTick; s.h = 0; s.growth = 0; s.firstResponse = true;
        s.weaponUntil = s.time + C.weaponWindow;
        log('E启动 / 续开：22秒巡衡；重置本轮成长，不产生归衡奖励');
        if (damage('ordinary', talent.initial, 'E初始')) particles(C.initialParticles);
        apply('E初始', 'active');
        return true;
      }
      if (hold) return true;
      return recastSkill();
    }
    function reaction(type, event = {}) {
      if (!['swirl', 'conduct'].includes(type)) throw new Error('未知反应');
      if (event.kind === 'damage' || event.owner && event.owner !== 'team') return reject('非本队真实反应，不写H');
      const id = event.id ?? `event-${++sequence}`;
      if (seen.has(id)) { s.metrics.duplicates++; log('同一输入事件已处理', 'duplicate'); return false; }
      seen.add(id);
      log(`${type}原生反应输入（${event.onField === false ? '后台' : '前台或未指定'}）`, 'reaction');
      // The artifact belongs to the wearer, not to the patrol state or route GCD.
      if (event.wearer === true) artifactTrigger();
      if (!patrol() || !s.targetValid || event.inRange === false) return reject('无巡衡或反应目标不在有效范围，不追加响应');
      if (!ready(s.lastRoute, C.routeCooldown)) { s.metrics.gcdBlocked++; return reject('原生反应保留；2.5秒响应间隔内'); }
      s.lastRoute = s.time;
      const first = s.firstResponse; s.firstResponse = false;
      const stride = first && config.constellation >= 1 ? 2 : 1;
      s.h = (s.mode === 'light' ? -1 : 1) * Math.min(2, Math.abs(s.h) + stride);
      s.growth = Math.max(s.growth, Math.abs(s.h));
      s.metrics.main++;
      const main = talent[s.mode] * (first && config.constellation >= 1 ? 1.2 : 1);
      damage(type, main, `${s.mode}主响应`);
      if (first) particles(C.firstResponseParticles);
      if (zero()) { s.metrics.companion++; damage(type, main * (config.constellation >= 6 ? C.c6Companion : C.companion), '伴随响应（无附着）'); }
      return true;
    }
    function burst() {
      if (!ready(s.lastBurst, C.burstCooldown)) return reject('Q冷却未好');
      if (s.energy + EPS < C.burstCost) return reject('能量不足50，拒绝Q；C4不能预支');
      s.onField = true; s.lastBurst = s.time; s.energy -= C.burstCost;
      if (patrol() && s.h) returnZero('Q');
      damage('ordinary', config.constellation >= 5 ? C.q13 : C.q10, 'Q初始');
      apply('Q初始');
      if (patrol()) s.zeroUntil = Math.min(s.patrolUntil, s.time + C.zero);
      if (config.constellation >= 4) { s.metrics.refund += C.c4Refund; addEnergy(C.c4Refund, 'C4支付后返还'); }
      return true;
    }
    function leave() {
      s.patrolUntil = 0; s.zeroUntil = 0; s.calibrationUntil = 0; s.weaponTeamUntil = 0;
      s.artifactUntil = 0; s.weaponUntil = 0; s.h = 0; s.growth = 0; s.nextTick = Infinity;
      log('死亡 / 离队：清空角色持续效果');
    }
    function setTarget(valid, id = s.targetId) { s.targetValid = Boolean(valid); s.targetId = id; log(`目标${id}：${valid ? '进入有效范围' : '离开或失效'}`); }
    function setOnField(value) { s.onField = Boolean(value); log(`娜蒂娅转为${s.onField ? '前台' : '后台'}`); }
    function externalEnergy(base, direct = 0) {
      if (![base, direct].every(n => Number.isFinite(n) && n >= 0)) throw new Error('能量输入须非负');
      addEnergy(base * config.er / 100 + direct, '外部基础能量×充能 + 直回');
    }
    function snapshot() {
      return JSON.parse(JSON.stringify({ ...s, nextTick: Number.isFinite(s.nextTick) ? s.nextTick : null,
        patrol: patrol(), zero: zero(), effects: effects(), config }));
    }
    return Object.freeze({ advance, castSkill, recastSkill, switchMode, reaction, burst,
      leave, setTarget, setOnField, externalEnergy, snapshot });
  }
  return Object.freeze({ C, create });
});
