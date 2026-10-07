import React, { useEffect, useRef, useState } from "react";

/* ---------------------------------------------------------
   Ember — an AI fire-safety companion (prototype)
   Canned, keyword-based responses stand in for a real model.
   Swap `answerFrom()` for a fetch to your own backend/API
   when you're ready to wire this up for real.
--------------------------------------------------------- */

const GREETING_LINES = [
  "Hi, I'm Ember.",
  "I keep watch for fire risk near you, day and night.",
];

const QUICK_ACTIONS = [
  {
    id: "risk",
    label: "Check my home's risk",
    prompt: "What's the fire risk near my home right now?",
  },
  {
    id: "report",
    label: "Report smoke or fire",
    prompt: "I want to report smoke or a fire.",
  },
  {
    id: "plan",
    label: "Build an evacuation plan",
    prompt: "Help me build an evacuation plan.",
  },
  {
    id: "gobag",
    label: "Review my go-bag checklist",
    prompt: "What should be in my go-bag?",
  },
];

const SENSORS = [
  { id: 1, label: "Backyard sensor", reading: "Clear", ok: true },
  { id: 2, label: "Garage sensor", reading: "Clear", ok: true },
  { id: 3, label: "Ridge weather station", reading: "Elevated wind", ok: false },
];

function answerFrom(raw) {
  const q = raw.toLowerCase();

  if (q.includes("report")) {
    return "Thanks for flagging it. If you can see active flames or heavy smoke right now, call your local emergency number first — I'll notify the nearest fire station with your saved location the moment you confirm.";
  }
  if (q.includes("evacuat") || q.includes("plan")) {
    return "Let's keep it simple: pick two exit routes from your home, agree on a meeting point with your household, and decide who grabs the go-bag. I can walk you through each step if you want.";
  }
  if (q.includes("go-bag") || q.includes("go bag") || q.includes("checklist")) {
    return "A solid go-bag covers water, a battery radio, copies of ID and insurance papers, medication, a phone charger, and a change of clothes for each person. Want me to turn this into a printable list?";
  }
  if (q.includes("risk") || q.includes("near") || q.includes("home")) {
    return "Your saved home is currently at moderate risk. A small brush fire was detected 2.4 miles out about 12 minutes ago, and wind is picking up on the ridge above you — I'll let you know if that changes.";
  }
  if (q.includes("smoke detector") || q.includes("alarm")) {
    return "Test each detector monthly and replace the batteries once a year — or sooner if you hear the low-battery chirp. Detectors themselves are good for about 10 years before the sensor wears out.";
  }
  if (q.includes("extinguish")) {
    return "For a small contained fire, keep a class ABC extinguisher within reach in the kitchen and garage. If the fire is bigger than a wastebasket, leave and call for help instead of fighting it.";
  }
  return "I don't have a canned answer for that yet in this prototype, but in a wired-up version I'd reason through it live. Try asking about evacuation plans, go-bags, smoke detectors, or the risk near your home.";
}

function useTypewriter(lines, speed = 28, lineGap = 500) {
  const [renderedLines, setRenderedLines] = useState([]);
  const [done, setDone] = useState(false);

  useEffect(() => {
    let cancelled = false;
    let lineIndex = 0;
    let charIndex = 0;
    let current = "";
    const built = [];

    function tick() {
      if (cancelled) return;
      if (lineIndex >= lines.length) {
        setDone(true);
        return;
      }
      const targetLine = lines[lineIndex];
      if (charIndex < targetLine.length) {
        current += targetLine[charIndex];
        charIndex += 1;
        setRenderedLines([...built, current]);
        setTimeout(tick, speed);
      } else {
        built.push(current);
        current = "";
        charIndex = 0;
        lineIndex += 1;
        setTimeout(tick, lineGap);
      }
    }
    const start = setTimeout(tick, 350);
    return () => {
      cancelled = true;
      clearTimeout(start);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { renderedLines, done };
}

function Orb({ awake }) {
  return (
    <div className={"orb" + (awake ? " orb--awake" : "")} aria-hidden="true">
      <div className="orb__core" />
      <div className="orb__ring orb__ring--1" />
      <div className="orb__ring orb__ring--2" />
    </div>
  );
}

function StatusRail({ visible }) {
  return (
    <ul className={"rail" + (visible ? " rail--visible" : "")}>
      {SENSORS.map((s) => (
        <li className="rail__item" key={s.id}>
          <span className={"rail__dot" + (s.ok ? "" : " rail__dot--warn")} />
          <span className="rail__label">{s.label}</span>
          <span className="rail__reading">{s.reading}</span>
        </li>
      ))}
    </ul>
  );
}

function RiskPanel() {
  return (
    <section className="panel panel--risk" aria-labelledby="risk-heading">
      <div className="panel__head">
        <h2 id="risk-heading">Your area</h2>
        <span className="badge badge--amber">Moderate risk</span>
      </div>

      <div className="risk-map" role="img" aria-label="Map showing a moderate fire risk 2.4 miles from your home">
        <svg viewBox="0 0 240 240" width="100%" height="100%">
          <circle cx="120" cy="120" r="108" className="ring ring--outer" />
          <circle cx="120" cy="120" r="70" className="ring ring--mid" />
          <circle cx="120" cy="120" r="34" className="ring ring--inner" />
          <circle cx="120" cy="120" r="5" className="pin pin--home" />
          <circle cx="176" cy="70" r="7" className="pin pin--hazard" />
        </svg>
        <div className="risk-map__legend">
          <span><i className="dot dot--home" /> Your home</span>
          <span><i className="dot dot--hazard" /> Detected hotspot</span>
        </div>
      </div>

      <p className="panel__note">
        A small brush fire was detected 2.4 miles from your saved home address.
        Local crews were notified 12 minutes ago, and wind on the ridge above
        you is picking up.
      </p>
    </section>
  );
}

function QuickActions({ onPick }) {
  return (
    <section className="panel panel--actions" aria-labelledby="actions-heading">
      <h2 id="actions-heading">What do you need?</h2>
      <div className="actions">
        {QUICK_ACTIONS.map((a) => (
          <button
            key={a.id}
            className="action"
            onClick={() => onPick(a.prompt)}
            type="button"
          >
            {a.label}
          </button>
        ))}
      </div>
    </section>
  );
}

function AskEmber({ messages, onSend }) {
  const [value, setValue] = useState("");
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  function submit(e) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
  }

  return (
    <section className="panel panel--chat" aria-labelledby="chat-heading">
      <h2 id="chat-heading">Ask Ember</h2>

      <div className="chat__list" ref={listRef}>
        {messages.length === 0 && (
          <p className="chat__empty">
            Ask about evacuation plans, go-bags, smoke detectors, or the risk
            near your home.
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={"chat__bubble chat__bubble--" + m.from}>
            {m.text}
          </div>
        ))}
      </div>

      <form className="chat__form" onSubmit={submit}>
        <input
          className="chat__input"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Ask Ember anything about fire safety…"
          aria-label="Ask Ember anything about fire safety"
        />
        <button className="chat__send" type="submit">
          Send
        </button>
      </form>
    </section>
  );
}

export default function App() {
  const { renderedLines, done } = useTypewriter(GREETING_LINES);
  const [messages, setMessages] = useState([]);

  function handleSend(text) {
    setMessages((prev) => [
      ...prev,
      { from: "user", text },
      { from: "ember", text: answerFrom(text) },
    ]);
  }

  return (
    <div className="page">
      <header className="hero">
        <Orb awake={done} />
        <div className="hero__text">
          {renderedLines.map((line, i) => (
            <p key={i} className="hero__line">
              {line}
              {i === renderedLines.length - 1 && !done && (
                <span className="cursor" aria-hidden="true" />
              )}
            </p>
          ))}
          <div className={"hero__badges" + (done ? " hero__badges--visible" : "")}>
            <span className="badge">3 sensors reporting</span>
            <span className="badge badge--ok">Air quality nominal</span>
          </div>
        </div>
        <StatusRail visible={done} />
      </header>

      <main className="dashboard">
        <RiskPanel />
        <div className="dashboard__side">
          <QuickActions onPick={handleSend} />
          <AskEmber messages={messages} onSend={handleSend} />
        </div>
      </main>

      <footer className="footer">
        <p>Ember is a prototype. In a real emergency, call your local emergency number.</p>
      </footer>
    </div>
  );
}
