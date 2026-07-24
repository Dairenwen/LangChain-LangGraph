import { useRef, useState } from "react";
import { ArrowUpRight, Upload } from "lucide-react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);
const DEFAULT_PROMPT = "我想在武汉租一套 1000-2000 元的房子，最好在街道口附近。";
export default function Hero({ onStart }: { onStart: (prompt: string) => void }) {
  const root = useRef<HTMLElement>(null); const input = useRef<HTMLInputElement>(null);
  const [prompt, setPrompt] = useState(DEFAULT_PROMPT); const [fileName, setFileName] = useState("");
  useGSAP(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const select = gsap.utils.selector(root); gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(select(".hero-nav"), { y: -20, autoAlpha: 0, duration: .65 })
      .from(select(".hero-copy"), { y: 28, autoAlpha: 0, duration: .72 }, "<.16")
      .from(select(".hero-prompt"), { y: 32, scale: .98, autoAlpha: 0, duration: .72 }, "<.08");
  }, { scope: root });
  const begin = () => onStart(prompt.trim() || DEFAULT_PROMPT);
  return <section ref={root} className="relative min-h-svh w-full overflow-hidden bg-wandor-dark">
    <video className="absolute inset-0 z-0 h-full w-full object-cover" src="https://pollen-batch-41236914.figma.site/_components/v2/f0ee2dae7671c170c34f12e31c4cb41418976c98/769c564298c132f7919405cd9f17c1b1231f341d.769c5642.mp4" autoPlay muted loop playsInline />
    <div className="pointer-events-none absolute inset-x-0 top-0 z-[1] h-[687px] bg-[linear-gradient(180deg,#fff_0%,transparent_100%)]" />
    <div className="relative z-[2] mx-auto max-w-[1360px]">
      <nav className="hero-nav relative flex items-center justify-between px-6 pb-4 pt-5 md:px-20 md:pt-6"><span className="select-none font-display text-[32px] leading-none text-black md:text-[40px]">wandor</span><div className="absolute left-1/2 hidden -translate-x-1/2 gap-8 md:flex">{["Discover", "Pricing", "FAQs"].map((item) => <button key={item} className="bg-transparent text-[15px] font-medium uppercase tracking-[.04em] text-wandor-text hover:opacity-55">{item}</button>)}</div><button onClick={begin} className="rounded-full bg-wandor-dark px-4 py-3 text-[13px] font-medium uppercase tracking-[.04em] text-[#fafafa] transition hover:bg-[#333] active:scale-95 md:px-5 md:py-3.5 md:text-[15px]">开始咨询</button></nav>
      <main className="hero-copy flex flex-col items-center px-6 pb-24 pt-16 text-center"><p className="mb-3 text-sm font-semibold uppercase tracking-[.18em] text-wandor-prompt">Your rental co-pilot</p><h1 className="mb-5 max-w-[820px] text-[clamp(40px,6vw,68px)] font-medium leading-[1.05] tracking-[-.04em] text-wandor-text">Where will you live next?</h1><p className="mb-10 max-w-[500px] text-xl font-medium leading-relaxed text-wandor-muted">告诉 AI 你想租在哪里、预算是多少，它会为你整理合适的房源与下一步建议。</p>
        <div className="hero-prompt will-transform relative min-h-[226px] w-[701px] overflow-hidden rounded-[44px] border-[3px] border-white bg-white/[.08] shadow backdrop-blur-[20px] max-md:w-[calc(100vw-48px)]"><textarea value={prompt} onChange={(event) => setPrompt(event.target.value.slice(0, gsap.utils.clamp(0, 600, event.target.value.length)))} className="absolute left-[29px] top-[27px] h-[89px] w-[609px] resize-none bg-transparent p-0 text-left text-xl font-medium leading-relaxed text-wandor-prompt outline-none max-md:w-[calc(100%-58px)] max-md:text-[17px]" aria-label="描述租房需求" /><input ref={input} type="file" accept="image/*,.pdf" className="hidden" onChange={(event) => setFileName(event.target.files?.[0]?.name ?? "")} /><button onClick={() => input.current?.click()} className="absolute left-[21px] top-[143px] flex h-11 w-11 items-center justify-center rounded-full border border-white/70 bg-transparent backdrop-blur hover:scale-105" aria-label="选择文件"><Upload className="h-[18px] w-[18px]" /></button>{fileName && <span className="absolute bottom-[34px] left-[76px] max-w-[270px] truncate text-xs text-wandor-text/70">已选择：{fileName}</span>}<button onClick={begin} className="absolute bottom-[21px] right-[21px] flex h-14 w-[156px] items-center justify-center gap-2 rounded-[44px] bg-black text-base font-medium text-[#fafafa] transition hover:bg-[#333] active:scale-95">开始咨询 <ArrowUpRight className="h-4 w-4" /></button></div><p className="mt-4 text-xs font-medium text-white/75">支持连续对话与中断后继续填写条件</p>
      </main>
    </div>
  </section>;
}
