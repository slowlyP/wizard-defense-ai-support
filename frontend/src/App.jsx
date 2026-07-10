import { useRef, useState } from "react";


const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

const EXAMPLES = [
  "레조넌스 했는데 재료만 사라졌어요",
  "마법사는 어디에 배치하는 게 좋아요?",
  "다음 층은 언제 열리나요?",
  "번개 마법사가 너무 강한 것 같아요",
];

const CATEGORY_LABELS = {
  gameplay_guide: "플레이 가이드",
  wizard_acquisition: "마법사 획득",
  wizard_growth: "마법사 성장",
  tower_progress: "타워 진행",
  skill_combat: "스킬·전투",
  bug_report: "오류 제보",
  feedback_balance: "밸런스 의견",
};

const URGENCY_LABELS = {
  low: "낮음",
  medium: "보통",
  high: "높음",
};

const RESPONSE_TYPE_LABELS = {
  guide_answer: "플레이 안내",
  acquisition_answer: "획득 안내",
  growth_answer: "성장 안내",
  tower_progress_answer: "타워 진행 안내",
  skill_combat_answer: "스킬·전투 안내",
  bug_triage: "오류 확인 요청",
  balance_feedback_ack: "밸런스 의견 접수",
};

function EnumCard({ label, value, translated, tone = "violet" }) {
  return (
    <article className={`result-card result-card--${tone}`}>
      <p className="result-label">{label}</p>
      <strong className="result-value">{translated}</strong>
      <code className="enum-value">원본 값 · {String(value)}</code>
    </article>
  );
}

function TextCard({ label, children, wide = false, highlighted = false }) {
  const classes = [
    "result-card",
    wide ? "result-card--wide" : "",
    highlighted ? "result-card--highlighted" : "",
  ]
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
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const textareaRef = useRef(null);

  const chooseExample = (example) => {
    setText(example);
    setError("");
    textareaRef.current?.focus();
  };

  const submitInquiry = async (event) => {
    event.preventDefault();
    const trimmedText = text.trim();

    if (!trimmedText) {
      setError("문의 내용을 입력해 주세요.");
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
        body: JSON.stringify({ text: trimmedText }),
      });

      if (!response.ok) {
        throw new Error("요청 실패");
      }

      setResult(await response.json());
    } catch {
      setResult(null);
      setError(
        "지원 분석 서버에 연결하지 못했습니다. 백엔드 실행 상태와 API 주소를 확인해 주세요.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <div className="ambient-rune ambient-rune--left" aria-hidden="true">✦</div>
      <div className="ambient-rune ambient-rune--right" aria-hidden="true">◇</div>

      <header className="hero">
        <div className="eyebrow"><span>✦</span> PC · 스팀 지원 도구 <span>✦</span></div>
        <h1>랜덤 마법사 디펜스 고객지원 미리보기</h1>
        <p>
          PC / Steam 방향의 문의 응답 초안을 미리 확인하는 포트폴리오용 도구
        </p>
      </header>

      <section className="workspace" aria-label="문의 분석 작업 공간">
        <form className="inquiry-panel" onSubmit={submitInquiry}>
          <div className="panel-heading">
            <div className="book-mark" aria-hidden="true">W</div>
            <div>
              <p className="section-kicker">마법 기록실</p>
              <h2>플레이 문의 입력</h2>
            </div>
          </div>

          <label htmlFor="inquiry">한국어 문의 내용</label>
          <textarea
            ref={textareaRef}
            id="inquiry"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="게임 플레이 중 궁금하거나 확인이 필요한 내용을 적어 주세요."
            rows="7"
            maxLength="1000"
          />
          <div className="input-meta">
            <span>게임 계정이나 결제 정보는 입력하지 마세요.</span>
            <span>{text.length} / 1000</span>
          </div>

          <div className="examples">
            <p>예시 문의</p>
            <div className="chip-list">
              {EXAMPLES.map((example) => (
                <button
                  type="button"
                  className="example-chip"
                  key={example}
                  onClick={() => chooseExample(example)}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {error && <div className="error-message" role="alert">{error}</div>}

          <button className="submit-button" type="submit" disabled={isLoading}>
            <span aria-hidden="true">✧</span>
            {isLoading ? "문의 분석 중..." : "문의 분석하기"}
          </button>
        </form>

        <section className="result-panel" aria-live="polite" aria-busy={isLoading}>
          <div className="result-heading">
            <div>
              <p className="section-kicker">지원 마법서</p>
              <h2>분석 결과</h2>
            </div>
            <span className={`status-orb ${result ? "status-orb--ready" : ""}`}>
              {result ? "분석 완료" : "입력 대기"}
            </span>
          </div>

          {!result && !isLoading && (
            <div className="empty-state">
              <div className="tower-glyph" aria-hidden="true">♜</div>
              <h3>문의가 도착하면 마법서가 열립니다</h3>
              <p>왼쪽에서 문의를 입력하거나 예시를 선택해 분석을 시작해 보세요.</p>
            </div>
          )}

          {isLoading && (
            <div className="loading-state" role="status">
              <span className="loading-rune" aria-hidden="true">✦</span>
              <p>문의 내용을 분석하고 응답 초안을 준비하고 있습니다...</p>
            </div>
          )}

          {result && !isLoading && (
            <div className="results-grid">
              <EnumCard
                label="예측 카테고리"
                value={result.predicted_category}
                translated={CATEGORY_LABELS[result.predicted_category] || "기타 문의"}
                tone="gold"
              />
              <EnumCard
                label="긴급도"
                value={result.urgency}
                translated={URGENCY_LABELS[result.urgency] || "확인 필요"}
                tone={result.urgency === "high" ? "rose" : "violet"}
              />
              <EnumCard
                label="사람 검토 필요"
                value={result.needs_human}
                translated={result.needs_human ? "필요" : "불필요"}
                tone={result.needs_human ? "rose" : "teal"}
              />
              <EnumCard
                label="응답 유형"
                value={result.suggested_response_type}
                translated={
                  RESPONSE_TYPE_LABELS[result.suggested_response_type] || "일반 안내"
                }
              />
              <TextCard label="라우팅 이유" wide>
                {result.routing_reason}
              </TextCard>
              <TextCard label="응답 초안" wide highlighted>
                {result.response_draft}
              </TextCard>
              <TextCard label="내부 메모" wide>
                {result.internal_note}
              </TextCard>
            </div>
          )}
        </section>
      </section>

      <footer className="portfolio-note">
        <span aria-hidden="true">◇</span>
        이 화면은 포트폴리오용 고객지원 미리보기이며 실제 고객지원, 계정 복구,
        결제 또는 문의 접수 시스템이 아닙니다.
      </footer>
    </main>
  );
}

export default App;
