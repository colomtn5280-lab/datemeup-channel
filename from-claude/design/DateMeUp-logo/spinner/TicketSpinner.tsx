// DateMeUp ticket spinner for React Native (iOS + Android).
// Deps: react-native-svg, react-native-reanimated (v3+). Respects Reduce Motion.
import React, { useEffect } from 'react';
import Svg, { Path, Circle, G } from 'react-native-svg';
import Animated, {
  useSharedValue, useAnimatedProps, withRepeat, withTiming, Easing, useReducedMotion, cancelAnimation,
} from 'react-native-reanimated';

const AG = Animated.createAnimatedComponent(G);
const AP = Animated.createAnimatedComponent(Path);
const TICKET = 'M14 22 H86 a5 5 0 0 1 5 5 V41 a8 8 0 0 0 0 16 V73 a5 5 0 0 1 -5 5 H14 a5 5 0 0 1 -5 -5 V57 a8 8 0 0 0 0 -16 V27 a5 5 0 0 1 5 -5 Z';
const C = { night: '#1E1A38', teal: '#0E8A86', coral: '#FF6B57', white: '#FFFFFF' };
const CYCLE = 1400;

// bob: 0→-5→0 during first 60% of the cycle, rest still (matches web keyframes)
function bob(p: number) {
  'worklet';
  const x = ((p % 1) + 1) % 1;
  if (x >= 0.6) return 0;
  const k = x / 0.6; // 0..1
  return -5 * Math.sin(Math.PI * k) ** 2;
}

export function TicketSpinner({ size = 64, onDark = false, label = 'Loading' }: { size?: number; onDark?: boolean; label?: string }) {
  const reduce = useReducedMotion();
  const t = useSharedValue(0);
  useEffect(() => {
    t.value = 0;
    t.value = withRepeat(withTiming(1, { duration: reduce ? 2000 : CYCLE, easing: Easing.linear }), -1, false);
    return () => cancelAnimation(t);
  }, [reduce]);

  const perf = useAnimatedProps(() => ({ strokeDashoffset: reduce ? 0 : -16 * t.value })); // 2 dash periods per cycle
  const a = useAnimatedProps(() => ({ transform: `translate(0 ${reduce ? 0 : bob(t.value)})`, opacity: reduce ? 0.775 + 0.225 * Math.cos(2 * Math.PI * t.value) : 1 }));
  const b = useAnimatedProps(() => ({ transform: `translate(0 ${reduce ? 0 : bob(t.value - 0.2 / 1.4)})` }));
  const bar1 = useAnimatedProps(() => ({ opacity: reduce ? 1 : (t.value % 1) < 0.5 ? 1 : 0.3 }));
  const bar2 = useAnimatedProps(() => ({ opacity: reduce ? 1 : ((t.value - 0.25 + 1) % 1) < 0.5 ? 1 : 0.3 }));

  return (
    <Svg width={size} height={size * 0.7} viewBox="5 15 90 70" accessible accessibilityRole="progressbar" accessibilityLabel={label}>
      <Path d={TICKET} fill={C.white} stroke={onDark ? undefined : C.night} strokeWidth={onDark ? 0 : 4} />
      <AP animatedProps={perf} d="M70 26 V74" stroke={C.night} strokeWidth={3} strokeDasharray="4 4" />
      <AG animatedProps={a}><Circle cx={31} cy={42} r={8} fill={C.teal} /><Path d="M18 74 A13 13 0 0 1 44 74 Z" fill={C.teal} /></AG>
      <AG animatedProps={b}><Circle cx={48} cy={44} r={8} fill={C.coral} /><Path d="M35 76 A13 13 0 0 1 61 76 Z" fill={C.coral} /></AG>
      <AP animatedProps={bar1} d="M77 44 v12" stroke={C.night} strokeWidth={3.5} strokeLinecap="round" />
      <AP animatedProps={bar2} d="M83 44 v12" stroke={C.night} strokeWidth={3.5} strokeLinecap="round" />
    </Svg>
  );
}

// Show only if loading takes > 300 ms (prevents a flash on fast loads); keep visible ≥ 500 ms once shown.
export function useDelayedSpinner(loading: boolean, delay = 300, minShow = 500) {
  const [show, setShow] = React.useState(false);
  const shownAt = React.useRef(0);
  useEffect(() => {
    let tm: ReturnType<typeof setTimeout>;
    if (loading) tm = setTimeout(() => { shownAt.current = Date.now(); setShow(true); }, delay);
    else if (show) tm = setTimeout(() => setShow(false), Math.max(0, minShow - (Date.now() - shownAt.current)));
    return () => clearTimeout(tm);
  }, [loading]);
  return show;
}
