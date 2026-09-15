const assert = require('node:assert/strict');
const {create, C} = require('./nadia_simulator_core.js');
let passed = 0;
function test(name, fn) { fn(); passed++; console.log(`PASS ${name}`); }
function near(a,b) {assert.ok(Math.abs(a-b)<1e-6, `${a} != ${b}`);}
function endpoint(m) {m.reaction('swirl');m.advance(2.5);m.reaction('conduct',{onField:false});}
test('C0 mixed front/back reactions reach selected endpoint; direct events do not',()=>{
 const m=create();m.castSkill();endpoint(m);assert.equal(m.snapshot().h,-2);assert.equal(m.snapshot().effects.characterBonus,50);
 m.advance(3);m.reaction('conduct',{kind:'damage'});assert.equal(m.snapshot().metrics.main,2);
});
test('dedup, GCD, outsider and range do not create extra responses',()=>{
 const m=create();m.castSkill();m.reaction('swirl',{id:'one'});m.reaction('conduct',{id:'two'});
 m.advance(3);m.reaction('conduct',{id:'one'});m.reaction('conduct',{owner:'outsider'});m.reaction('conduct',{inRange:false});
 assert.equal(m.snapshot().metrics.main,1);assert.equal(m.snapshot().metrics.duplicates,1);assert.equal(m.snapshot().metrics.gcdBlocked,1);
});
test('return retains growth; switch gives no rewards; base shred persists',()=>{
 const m=create();m.castSkill();endpoint(m);m.recastSkill();let s=m.snapshot();assert.equal(s.h,0);assert.equal(s.effects.characterBonus,70);
 m.switchMode();s=m.snapshot();assert.equal(s.metrics.full,1);assert.equal(s.effects.shred.electro,30);assert.equal(s.effects.shred.anemo,0);
 m.advance(8);assert.equal(m.snapshot().effects.characterBonus,50);
});
test('renew at18 keeps single patrol;22 expiry clears all character effects',()=>{
 const m=create();m.castSkill();endpoint(m);m.advance(15.5);m.castSkill();let s=m.snapshot();assert.equal(s.patrolUntil,40);assert.equal(s.growth,0);
 m.advance(22);s=m.snapshot();assert.equal(s.effects.characterBonus,0);assert.equal(s.zero,false);assert.equal(s.h,0);
});
test('Q exact end does not skip scheduled tick; Q itself does not reschedule',()=>{
 const m=create();m.castSkill();m.advance(1.5);m.burst();assert.equal(m.snapshot().nextTick,3.5);
 m.advance(12);const ticks=m.snapshot().events.filter(e=>e.kind==='damage'&&e.text.startsWith('自动刻度'));
 assert.ok(ticks.some(e=>e.time===12.5));assert.equal(m.snapshot().nextTick,14);
 m.advance(.5);assert.equal(m.snapshot().nextTick,16);
 const n=create();n.castSkill();n.advance(0);n.burst();n.advance(12);assert.ok(n.snapshot().events.some(e=>e.time===12&&e.text.startsWith('自动刻度')&&e.kind==='damage'));assert.equal(n.snapshot().nextTick,14);
});
test('no target gives no initial particles; return/companions do not add attachment',()=>{
 const m=create();m.setTarget(false);m.castSkill();m.advance(5);assert.equal(m.snapshot().metrics.particles,0);assert.equal(m.snapshot().metrics.applications,0);
 m.setTarget(true,'new');assert.equal(m.snapshot().effects.shred.cryo,30);m.reaction('conduct');assert.equal(m.snapshot().metrics.particles,1);
 const a=m.snapshot().metrics.applications;m.reaction('swirl');assert.equal(m.snapshot().metrics.applications,a);
 m.setTarget(false);assert.equal(m.snapshot().effects.shred.cryo,0);
});
test('C1 first response only, C3/C5 talent tables, C2/C6 elevation not additive',()=>{
 for(let c=0;c<=6;c++){
  const m=create({constellation:c});m.castSkill();m.reaction('swirl');let s=m.snapshot();assert.equal(s.h,c?-2:-1);
  near(s.coefficients.swirl,(c>=3?79:70)*(c?1.2:1));assert.equal(s.effects.elevation,c>=6?25:c>=2?15:0);
  m.burst();s=m.snapshot();assert.equal(s.coefficients.ordinary,(c>=3?114:101)+(c?(c>=3?214:190):150)+(c>=5?405:360));
  m.advance(2.5);m.reaction('conduct');assert.equal(m.snapshot().h,-1);
 }
});
test('C4 cannot prepay Q; refunds8 after successful payment',()=>{
 const m=create({constellation:4,energy:42});assert.equal(m.burst(),false);m.externalEnergy(0,8);assert.equal(m.burst(),true);assert.equal(m.snapshot().energy,8);
 assert.equal(m.burst(),false);assert.equal(m.snapshot().metrics.refund,8);
});
test('equipment is post-hit; wearer reaction triggers artifact inside GCD',()=>{
 const m=create({weapon:true,artifact:true});m.castSkill();m.setOnField(false);m.reaction('swirl');let s=m.snapshot();let hit=s.events.find(e=>e.kind==='damage'&&e.type==='swirl');assert.equal(hit.artifactBonus,0);assert.equal(hit.weaponTeamBonus,0);
 assert.equal(s.effects.artifactTeamBonus,50);assert.equal(s.effects.weaponTeamBonus,12);
 m.advance(1);m.reaction('swirl',{wearer:true});assert.equal(m.snapshot().artifactUntil,13);
});
test('C6 does not double Cryo shred; death clears all ongoing character effects',()=>{
 const m=create({constellation:6});m.castSkill();endpoint(m);m.burst();assert.deepEqual(m.snapshot().effects.shred,{cryo:30,anemo:30,electro:30});
 m.leave();m.advance(10);assert.equal(m.snapshot().effects.characterBonus,0);assert.equal(m.snapshot().effects.elevation,0);assert.equal(m.snapshot().zero,false);
});
test('energy inputs validated; background particle factor explicit',()=>{
 const m=create({energy:0,er:100});m.castSkill();assert.equal(m.snapshot().energy,12);m.setOnField(false);m.reaction('swirl');near(m.snapshot().energy,13.8);
 assert.throws(()=>m.advance(-1));assert.throws(()=>m.externalEnergy(-1));
});
test('no-Q full20s support coverage and independent 10 tick applications',()=>{
 const m=create();m.castSkill();endpoint(m);m.advance(17.5);let s=m.snapshot();near(s.metrics.patrolSeconds,20);near(s.metrics.shredSeconds,20);assert.equal(s.metrics.ticks,10);assert.equal(s.metrics.applications,11);assert.equal(s.effects.characterBonus,50);
});
test('wearer artifact works without patrol and Q window is clipped by patrol',()=>{
 const m=create({artifact:true});m.reaction('conduct',{wearer:true});assert.equal(m.snapshot().effects.artifactTeamBonus,50);assert.equal(m.snapshot().h,0);
 m.castSkill();m.advance(20);m.burst();assert.equal(m.snapshot().zeroUntil,22);m.advance(2);assert.equal(m.snapshot().zero,false);
});
test('return reward throttle is independent from H reset; switch cannot farm particles',()=>{
 const m=create();m.castSkill();endpoint(m);m.recastSkill();m.advance(2.5);m.reaction('swirl');m.burst();assert.equal(m.snapshot().h,0);assert.equal(m.snapshot().metrics.full,1);assert.equal(m.snapshot().metrics.normal,0);
 const n=m.snapshot().metrics.particles;m.castSkill(true);m.advance(1);m.castSkill(true);assert.equal(m.snapshot().metrics.particles,n);
});
test('fresh instance has no shared route state; multi-rotation energy is explicit',()=>{
 const a=create({energy:0,er:100});a.castSkill();endpoint(a);a.externalEnergy(0,35);a.burst();assert.equal(a.snapshot().energy,0);
 a.advance(17.5);a.castSkill();endpoint(a);assert.equal(a.burst(),false);a.externalEnergy(0,35);assert.equal(a.burst(),true);
 const b=create();assert.equal(b.snapshot().h,0);assert.equal(b.snapshot().metrics.particles,0);
});
console.log(`${passed} rule scenarios passed. Native reactions and team DPS are not simulated.`);
