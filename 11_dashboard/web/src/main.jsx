import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowRight,
  Check,
  Clipboard,
  FileCheck2,
  Lock,
  Play,
  RefreshCw,
  ShieldCheck,
  Upload,
} from 'lucide-react';
import './styles.css';

const STAGES = [
  ['intake', '赛题接入'],
  ['data_analysis', '数据分析'],
  ['model_design', '模型设计'],
  ['implementation', '代码实现'],
  ['result_freeze', '结果冻结'],
  ['evidence_design', '证据设计'],
  ['paper_review', '论文审查'],
  ['finalize', '终稿导出'],
];

const STATUS_LABELS = {
  pending_chatgpt: '等待 ChatGPT',
  pending_codex: '等待 Codex',
  blocked: '已阻塞',
  pending_human: '等待人工确认',
  completed: '全部完成',
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

function StatusMark({ tone = 'quiet', children }) {
  return <span className={`status-mark ${tone}`}>{children}</span>;
}

function StageRail({ state }) {
  const completed = new Set(state?.completed_stages || []);
  const currentIndex = STAGES.findIndex(([id]) => id === state?.current_stage);
  return (
    <nav className="stage-rail" aria-label="正式工作流阶段">
      <div className="rail-heading">正式流水线</div>
      {STAGES.map(([id, label], index) => {
        const done = completed.has(id) || (state?.status === 'completed' && index <= currentIndex);
        const current = state?.current_stage === id;
        const locked = !done && !current;
        return (
          <div className={`stage-line ${current ? 'current' : ''}`} key={id}>
            <span className={`stage-index ${done ? 'done' : current ? 'active' : ''}`}>
              {done ? <Check size={13} /> : locked ? <Lock size={11} /> : index + 1}
            </span>
            <span className="stage-copy">
              <strong>{label}</strong>
              <small>{id}</small>
            </span>
          </div>
        );
      })}
      <div className="rail-rule" />
      <p>ChatGPT 决策与写作<br />Codex 复现与核验</p>
    </nav>
  );
}

function TextArtifact({ label, value, onCopy }) {
  if (!value) return null;
  return (
    <section className="artifact-block">
      <div className="artifact-heading">
        <span>{label}</span>
        <button className="icon-action" onClick={() => onCopy(value)} title={`复制${label}`}>
          <Clipboard size={15} />
        </button>
      </div>
      <pre>{value}</pre>
    </section>
  );
}

function HandoffHistory({ rows, selected, onSelect }) {
  return (
    <aside className="inspector">
      <div className="inspector-heading">
        <span>交接记录</span>
        <StatusMark>{rows.length}</StatusMark>
      </div>
      <div className="handoff-list">
        {rows.length === 0 && <p className="empty-copy">尚未生成交接包。</p>}
        {rows.map((row) => (
          <button
            key={row.handoff_id}
            className={`handoff-row ${selected === row.handoff_id ? 'selected' : ''}`}
            onClick={() => onSelect(row.handoff_id)}
          >
            <span>
              <strong>{row.stage}</strong>
              <small>{row.handoff_id}</small>
            </span>
            <StatusMark tone={row.status?.includes('pass') ? 'ok' : 'quiet'}>{row.status}</StatusMark>
          </button>
        ))}
      </div>
    </aside>
  );
}

function App() {
  const [state, setState] = useState(null);
  const [handoffs, setHandoffs] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [detail, setDetail] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [reportText, setReportText] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState('');
  const [checkResult, setCheckResult] = useState(null);

  const currentLabel = useMemo(
    () => STAGES.find(([id]) => id === state?.current_stage)?.[1] || state?.current_stage || '未初始化',
    [state],
  );

  async function load() {
    const [nextState, nextHandoffs] = await Promise.all([api('/api/state'), api('/api/handoffs')]);
    setState(nextState);
    setHandoffs(nextHandoffs);
    const nextSelected = selectedId || nextState.active_handoff_id || nextHandoffs[0]?.handoff_id || '';
    setSelectedId(nextSelected);
    if (nextSelected) setDetail(await api(`/api/handoffs/${encodeURIComponent(nextSelected)}`));
    else setDetail(null);
  }

  useEffect(() => {
    load().catch((error) => setNotice(error.message));
  }, []);

  async function selectHandoff(id) {
    setSelectedId(id);
    setDetail(await api(`/api/handoffs/${encodeURIComponent(id)}`));
  }

  async function action(path, payload, success) {
    setBusy(true);
    setNotice('');
    try {
      const result = await api(path, { method: 'POST', body: JSON.stringify(payload) });
      setNotice(success);
      await load();
      return result;
    } catch (error) {
      setNotice(error.message);
      throw error;
    } finally {
      setBusy(false);
    }
  }

  async function prepareChatGPT() {
    const result = await action('/api/actions/prepare', { target: 'chatgpt' }, 'ChatGPT 提示词包已生成');
    setSelectedId(result.handoff_id);
  }

  async function importResponse() {
    await action(
      '/api/actions/import',
      { handoff_id: state.active_handoff_id, response_text: responseText },
      'ChatGPT 回复已锁定并进入 Codex 验证',
    );
    setResponseText('');
  }

  async function prepareCodex() {
    await action(
      '/api/actions/prepare',
      { target: 'codex', handoff_id: state.active_handoff_id },
      'Codex 验证任务已生成',
    );
  }

  async function verifyCodex() {
    let report;
    try {
      report = JSON.parse(reportText);
    } catch {
      setNotice('Codex 回执必须是有效 JSON');
      return;
    }
    await action(
      '/api/actions/verify',
      { handoff_id: state.active_handoff_id, report },
      'Codex 回执已校验并记录',
    );
    setReportText('');
  }

  async function confirmGate() {
    await action(
      '/api/actions/confirm',
      { gate: state.pending_gate, confirmation },
      '人工闸门已确认',
    );
    setConfirmation('');
  }

  async function runCheck(kind) {
    const result = await action(`/api/actions/check-${kind}`, {}, `${kind === 'gates' ? '门禁' : '合同'}检查完成`);
    setCheckResult(result);
  }

  async function copy(value) {
    await navigator.clipboard.writeText(value);
    setNotice('已复制到剪贴板');
  }

  const prompt = detail?.['chatgpt_prompt.md'] || '';
  const codexTask = detail?.['codex_task.md'] || '';
  const receipt = detail?.['codex_receipt.json'] || '';

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">M</span>
          <span><strong>Math Workflow</strong><small>formal / v4</small></span>
        </div>
        <div className="topbar-status">
          <StatusMark tone={state?.status === 'blocked' ? 'danger' : state?.status === 'pending_human' ? 'warn' : 'ok'}>
            {STATUS_LABELS[state?.status] || '加载中'}
          </StatusMark>
          <button className="icon-action" onClick={() => load()} disabled={busy} title="刷新状态">
            <RefreshCw size={16} />
          </button>
        </div>
      </header>

      <div className="workspace-grid">
        <StageRail state={state} />

        <main className="workbench">
          <section className="stage-header">
            <div>
              <span className="eyebrow">当前阶段 · {state?.current_stage}</span>
              <h1>{currentLabel}</h1>
              <p>项目 {state?.project_id || '—'} · 所有事实以本地代码、文件与合同为准。</p>
            </div>
            <div className="stage-number">{String(Math.max(1, STAGES.findIndex(([id]) => id === state?.current_stage) + 1)).padStart(2, '0')}</div>
          </section>

          {notice && <div className="notice" role="status">{notice}</div>}

          <section className="action-surface">
            {state?.status === 'pending_chatgpt' && !state.active_handoff_id && (
              <div className="next-action">
                <div><span>下一动作</span><h2>生成 ChatGPT 推理包</h2><p>系统将冻结当前上下文哈希，并生成只包含结果、边界与验收定义的提示词。</p></div>
                <button className="primary-action" onClick={prepareChatGPT} disabled={busy}><Play size={17} />生成提示词</button>
              </div>
            )}

            {state?.status === 'pending_chatgpt' && state.active_handoff_id && (
              <>
                <div className="next-action compact"><div><span>等待网页端</span><h2>提交给 ChatGPT 后导入原始回复</h2></div></div>
                <TextArtifact label="ChatGPT 提示词" value={prompt} onCopy={copy} />
                <label className="input-label">ChatGPT 原始回复</label>
                <textarea value={responseText} onChange={(event) => setResponseText(event.target.value)} placeholder="粘贴包含正确 metadata 的完整回复…" />
                <button className="primary-action" onClick={importResponse} disabled={busy || !responseText.trim()}><Upload size={17} />锁定并导入</button>
              </>
            )}

            {state?.status === 'pending_codex' && (
              <>
                <div className="next-action compact"><div><span>本地验证</span><h2>让 Codex 执行证据核验</h2><p>模型冲突必须退回ChatGPT；Codex只能直接修复实现层问题。</p></div></div>
                {!codexTask && <button className="primary-action" onClick={prepareCodex} disabled={busy}><FileCheck2 size={17} />生成 Codex 任务</button>}
                <TextArtifact label="Codex 验证任务" value={codexTask} onCopy={copy} />
                <label className="input-label">Codex 回执 JSON</label>
                <textarea className="short" value={reportText} onChange={(event) => setReportText(event.target.value)} placeholder='{"verdict":"pass","checks":[],"artifacts":[],"contract_rows":[],"conflicts":[],"next_action":"advance"}' />
                <button className="primary-action" onClick={verifyCodex} disabled={busy || !reportText.trim()}><ShieldCheck size={17} />验证并记录</button>
              </>
            )}

            {state?.status === 'pending_human' && (
              <div className="gate-surface">
                <span>人工闸门</span>
                <h2>{state.pending_gate}</h2>
                <p>检查正式产物与Codex回执后，输入完整闸门名称。任何AI都不能代替你确认。</p>
                <input value={confirmation} onChange={(event) => setConfirmation(event.target.value)} placeholder={state.pending_gate} />
                <button className="primary-action" onClick={confirmGate} disabled={busy || confirmation !== state.pending_gate}><ArrowRight size={17} />确认并推进</button>
              </div>
            )}

            {state?.status === 'blocked' && (
              <div className="blocked-surface"><span>流程已停止</span><h2>需要补充证据或人工处理</h2><p>查看最近回执中的冲突和下一动作；状态不会自动前进。</p><TextArtifact label="Codex 回执" value={receipt} onCopy={copy} /></div>
            )}

            {state?.status === 'completed' && (
              <div className="complete-surface"><Check size={22} /><h2>正式流水线已完成</h2><p>最终提交仍以人工确认的提交包为准。</p></div>
            )}
          </section>

          <section className="verification-strip">
            <div><span>独立检查</span><p>不推进状态，只刷新合同与门禁报告。</p></div>
            <div className="strip-actions">
              <button onClick={() => runCheck('contracts')} disabled={busy}>检查合同</button>
              <button onClick={() => runCheck('gates')} disabled={busy}>检查门禁</button>
            </div>
          </section>
          {checkResult && <pre className="check-output">{JSON.stringify(checkResult, null, 2)}</pre>}
        </main>

        <HandoffHistory rows={handoffs} selected={selectedId} onSelect={(id) => selectHandoff(id).catch((error) => setNotice(error.message))} />
      </div>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
