import { useEffect, useRef, useState } from "react";


const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

const COPY = {
  ko: {
    documentTitle: "랜덤 마법사 디펜스 고객지원 미리보기",
    languageSelector: "언어 선택",
    eyebrow: "PC · 스팀 지원 도구",
    title: "랜덤 마법사 디펜스 고객지원 미리보기",
    subtitle: "PC / Steam 방향의 문의 응답 초안을 미리 확인하는 포트폴리오용 도구",
    inputKicker: "마법 기록실",
    inputTitle: "플레이 문의 입력",
    inputLabel: "한국어 문의 내용",
    placeholder: "게임 플레이 중 궁금하거나 확인이 필요한 내용을 적어 주세요.",
    privacy: "게임 계정이나 결제 정보는 입력하지 마세요.",
    examplesLabel: "예시 문의",
    examples: [
      "레조넌스 했는데 재료만 사라졌어요",
      "마법사는 어디에 배치하는 게 좋아요?",
      "다음 층은 언제 열리나요?",
      "번개 마법사가 너무 강한 것 같아요",
    ],
    emptyError: "문의 내용을 입력해 주세요.",
    connectionError: "지원 분석 서버에 연결하지 못했습니다. 백엔드 실행 상태와 API 주소를 확인해 주세요.",
    submit: "문의 분석하기",
    submitting: "문의 분석 중...",
    resultKicker: "지원 마법서",
    resultTitle: "분석 결과",
    ready: "분석 완료",
    waiting: "입력 대기",
    emptyTitle: "문의가 도착하면 마법서가 열립니다",
    emptyCopy: "왼쪽에서 문의를 입력하거나 예시를 선택해 분석을 시작해 보세요.",
    loading: "문의 내용을 분석하고 응답 초안을 준비하고 있습니다...",
    predictedCategory: "예측 카테고리",
    urgency: "긴급도",
    humanReview: "사람 검토 필요",
    responseType: "응답 유형",
    routingReason: "라우팅 이유",
    responseDraft: "응답 초안",
    internalNote: "내부 메모",
    originalValue: "원본 값",
    required: "필요",
    notRequired: "불필요",
    unknown: "확인 필요",
    general: "일반 안내",
    footer: "이 화면은 포트폴리오용 고객지원 미리보기이며 실제 고객지원, 계정 복구, 결제 또는 문의 접수 시스템이 아닙니다.",
    categoryLabels: {
      gameplay_guide: "플레이 가이드",
      wizard_acquisition: "마법사 획득",
      wizard_growth: "마법사 성장",
      tower_progress: "타워 진행",
      skill_combat: "스킬·전투",
      bug_report: "버그 제보",
      feedback_balance: "밸런스 의견",
    },
    urgencyLabels: { low: "낮음", medium: "보통", high: "높음" },
    responseTypeLabels: {
      guide_answer: "플레이 안내",
      acquisition_answer: "획득 안내",
      growth_answer: "성장 안내",
      tower_progress_answer: "타워 진행 안내",
      skill_combat_answer: "스킬·전투 안내",
      bug_triage: "오류 확인 요청",
      balance_feedback_ack: "밸런스 의견 접수",
    },
  },
  en: {
    documentTitle: "Random Wizard Defense Support Preview",
    languageSelector: "Language selection",
    eyebrow: "PC · Steam Support Tool",
    title: "Random Wizard Defense Support Preview",
    subtitle: "A portfolio tool for previewing PC / Steam-oriented support response drafts.",
    inputKicker: "Arcane Records",
    inputTitle: "Player Inquiry",
    inputLabel: "Player inquiry",
    placeholder: "Describe the player inquiry here.",
    privacy: "Do not enter game account or payment information.",
    examplesLabel: "Example inquiries",
    examples: [
      "Resonance consumed materials but nothing changed",
      "Where should I place my wizards?",
      "When does the next floor unlock?",
      "Lightning wizard feels too strong",
    ],
    emptyError: "Please enter a player inquiry.",
    connectionError: "Could not connect to the support analysis server. Check the backend status and API address.",
    submit: "Analyze inquiry",
    submitting: "Analyzing inquiry...",
    resultKicker: "Support Grimoire",
    resultTitle: "Analysis Result",
    ready: "Analysis complete",
    waiting: "Waiting for input",
    emptyTitle: "The support grimoire opens when an inquiry arrives",
    emptyCopy: "Enter an inquiry or select an example on the left to begin.",
    loading: "Analyzing the inquiry and preparing a response draft...",
    predictedCategory: "Predicted category",
    urgency: "Urgency",
    humanReview: "Human review",
    responseType: "Response type",
    routingReason: "Routing reason",
    responseDraft: "Response draft",
    internalNote: "Internal note",
    originalValue: "Original value",
    required: "Required",
    notRequired: "Not required",
    unknown: "Needs confirmation",
    general: "General guidance",
    footer: "This is a portfolio support preview, not a real customer support, account recovery, payment, or ticket submission system.",
    categoryLabels: {
      gameplay_guide: "Gameplay guide",
      wizard_acquisition: "Wizard acquisition",
      wizard_growth: "Wizard growth",
      tower_progress: "Tower progression",
      skill_combat: "Skills and combat",
      bug_report: "Bug report",
      feedback_balance: "Balance feedback",
    },
    urgencyLabels: { low: "Low", medium: "Medium", high: "High" },
    responseTypeLabels: {
      guide_answer: "Gameplay guidance",
      acquisition_answer: "Acquisition guidance",
      growth_answer: "Growth guidance",
      tower_progress_answer: "Tower progression guidance",
      skill_combat_answer: "Skill and combat guidance",
      bug_triage: "Bug triage",
      balance_feedback_ack: "Balance feedback acknowledgment",
    },
    routingReasons: {
      gameplay_guide: "This inquiry is routed to gameplay guidance because it concerns play methods, placement, composition, or strategy.",
      wizard_acquisition: "This inquiry is routed to acquisition guidance because it concerns wizard summons, acquisition, grades, or appearance rates.",
      wizard_growth: "This inquiry is routed to growth guidance because it concerns levels, experience, growth materials, or resonance.",
      tower_progress: "This inquiry is routed to tower guidance because it concerns floor progression, unlocks, bosses, or rewards.",
      skill_combat: "This inquiry is routed to skill and combat guidance because it concerns effects, cooldowns, damage, or targeting.",
      bug_report: "This inquiry includes an error or failure signal and is routed to bug triage for review.",
      feedback_balance: "This inquiry evaluates strength, cost, rates, or efficiency and is routed to balance feedback review.",
    },
  },
};

function getInitialLanguage() {
  try {
    return localStorage.getItem("wizard-support-language") === "en" ? "en" : "ko";
  } catch {
    return "ko";
  }
}

function EnumCard({ label, value, translated, originalValueLabel, tone = "violet" }) {
  return (
    <article className={`result-card result-card--${tone}`}>
      <p className="result-label">{label}</p>
      <strong className="result-value">{translated}</strong>
      <code className="enum-value">{originalValueLabel} · {String(value)}</code>
    </article>
  );
}

function TextCard({ label, children, wide = false, highlighted = false }) {
  const classes = ["result-card", wide && "result-card--wide", highlighted && "result-card--highlighted"]
    .filter(Boolean)
    .join(" ");
  return (
    <article className={classes}>
      <p className="result-label">{label}</p>
      <p className="result-copy">{children}</p>
    </article>
  );
}

function App() {
  const [language, setLanguage] = useState(getInitialLanguage);
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const textareaRef = useRef(null);
  const t = COPY[language];

  useEffect(() => {
    document.documentElement.lang = language;
    document.title = t.documentTitle;
    try {
      localStorage.setItem("wizard-support-language", language);
    } catch {
      // Language selection still works when browser storage is unavailable.
    }
  }, [language, t.documentTitle]);

  const changeLanguage = (nextLanguage) => {
    setLanguage(nextLanguage);
    setText("");
    setResult(null);
    setError("");
  };

  const chooseExample = (example) => {
    setText(example);
    setError("");
    textareaRef.current?.focus();
  };

  const submitInquiry = async (event) => {
    event.preventDefault();
    const trimmedText = text.trim();
    if (!trimmedText) {
      setError(t.emptyError);
      setResult(null);
      textareaRef.current?.focus();
      return;
    }

    setIsLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE_URL}/support/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: trimmedText, language }),
      });
      if (!response.ok) throw new Error("request failed");
      setResult(await response.json());
    } catch {
      setResult(null);
      setError(t.connectionError);
    } finally {
      setIsLoading(false);
    }
  };

  const displayedRoutingReason = result
    ? language === "en"
      ? t.routingReasons[result.predicted_category] || "This inquiry was routed using the local support rules."
      : result.routing_reason
    : "";

  return (
    <main className="app-shell">
      <div className="ambient-rune ambient-rune--left" aria-hidden="true">✦</div>
      <div className="ambient-rune ambient-rune--right" aria-hidden="true">◇</div>

      <nav className="language-switcher" aria-label={t.languageSelector}>
        <button type="button" className={language === "ko" ? "is-active" : ""} aria-pressed={language === "ko"} onClick={() => changeLanguage("ko")}>한국어</button>
        <button type="button" className={language === "en" ? "is-active" : ""} aria-pressed={language === "en"} onClick={() => changeLanguage("en")}>English</button>
      </nav>

      <header className="hero">
        <div className="eyebrow"><span>✦</span> {t.eyebrow} <span>✦</span></div>
        <h1>{t.title}</h1>
        <p>{t.subtitle}</p>
      </header>

      <section className="workspace" aria-label={t.inputTitle}>
        <form className="inquiry-panel" onSubmit={submitInquiry}>
          <div className="panel-heading">
            <div className="book-mark" aria-hidden="true">W</div>
            <div><p className="section-kicker">{t.inputKicker}</p><h2>{t.inputTitle}</h2></div>
          </div>

          <label htmlFor="inquiry">{t.inputLabel}</label>
          <textarea ref={textareaRef} id="inquiry" value={text} onChange={(event) => setText(event.target.value)} placeholder={t.placeholder} rows="7" maxLength="1000" />
          <div className="input-meta"><span>{t.privacy}</span><span>{text.length} / 1000</span></div>

          <div className="examples">
            <p>{t.examplesLabel}</p>
            <div className="chip-list">
              {t.examples.map((example) => (
                <button type="button" className="example-chip" key={example} onClick={() => chooseExample(example)}>{example}</button>
              ))}
            </div>
          </div>

          {error && <div className="error-message" role="alert">{error}</div>}
          <button className="submit-button" type="submit" disabled={isLoading}><span aria-hidden="true">✧</span> {isLoading ? t.submitting : t.submit}</button>
        </form>

        <section className="result-panel" aria-live="polite" aria-busy={isLoading}>
          <div className="result-heading">
            <div><p className="section-kicker">{t.resultKicker}</p><h2>{t.resultTitle}</h2></div>
            <span className={`status-orb ${result ? "status-orb--ready" : ""}`}>{result ? t.ready : t.waiting}</span>
          </div>

          {!result && !isLoading && <div className="empty-state"><div className="tower-glyph" aria-hidden="true">♜</div><h3>{t.emptyTitle}</h3><p>{t.emptyCopy}</p></div>}
          {isLoading && <div className="loading-state" role="status"><span className="loading-rune" aria-hidden="true">✦</span><p>{t.loading}</p></div>}

          {result && !isLoading && (
            <div className="results-grid">
              <EnumCard label={t.predictedCategory} value={result.predicted_category} translated={t.categoryLabels[result.predicted_category] || t.unknown} originalValueLabel={t.originalValue} tone="gold" />
              <EnumCard label={t.urgency} value={result.urgency} translated={t.urgencyLabels[result.urgency] || t.unknown} originalValueLabel={t.originalValue} tone={result.urgency === "high" ? "rose" : "violet"} />
              <EnumCard label={t.humanReview} value={result.needs_human} translated={result.needs_human ? t.required : t.notRequired} originalValueLabel={t.originalValue} tone={result.needs_human ? "rose" : "teal"} />
              <EnumCard label={t.responseType} value={result.suggested_response_type} translated={t.responseTypeLabels[result.suggested_response_type] || t.general} originalValueLabel={t.originalValue} />
              <TextCard label={t.routingReason} wide>{displayedRoutingReason}</TextCard>
              <TextCard label={t.responseDraft} wide highlighted>{result.response_draft}</TextCard>
              <TextCard label={t.internalNote} wide>{result.internal_note}</TextCard>
            </div>
          )}
        </section>
      </section>

      <footer className="portfolio-note"><span aria-hidden="true">◇</span>{t.footer}</footer>
    </main>
  );
}

export default App;
