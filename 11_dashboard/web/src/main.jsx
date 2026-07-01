import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  Activity,
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Clock3,
  Database,
  Eye,
  FileText,
  FlaskConical,
  Gauge,
  GitBranch,
  Hammer,
  History,
  ListChecks,
  Loader2,
  Lock,
  Play,
  RefreshCcw,
  ShieldCheck,
  SquareTerminal,
  XCircle
} from 'lucide-react';
import './styles.css';

const TABS = ['Contracts', 'Review', 'Figures', 'Prior DB', 'Learning', 'Logs', 'Workflow'];

const STAGE_LABELS = {
  latex_template: 'LaTeX 模板',
  intake: '题目读取',
  eda: '数据体检',
  task_analysis: '分问拆解',
  prior_retrieval: 'Prior 检索',
  model_route: '模型路由',
  codegen: '代码生成',
  results_freeze: '结果冻结',
  figures: '图表生成',
  paper_draft: '分段初稿',
  paper_full: '全文组装',
  auto_review: '自动审稿',
  revision: '修订闭环',
  polish: '事实润色',
  compile: '编译检查',
  final_export: '终稿导出'
};

const CHECK_ACTIONS = [
  { id: 'check-gates', label: 'Gate 检查', icon: ShieldCheck },
  { id: 'validate-contracts', label: '合同校验', icon: ClipboardCheck },
  { id: 'check-skill-router', label: 'Skill Router', icon: GitBranch },
  { id: 'validate-export', label: '导出结构', icon: ListChecks }
];

const RUN_DETAIL_TABS = ['Manifest', 'Revision Queue', 'Gap Report', 'Validation', 'Copy Risk', 'Full Gap'];

function statusTone(status) {
  const text = String(status || '').toLowerCase();
  if (text.includes('fail') || text.includes('blocked')) return 'danger';
  if (text.includes('warn') || text.includes('waiting') || text.includes('pending')) return 'warn';
  if (text.includes('pass') || text.includes('complete') || text.includes('confirmed')) return 'ok';
  if (text.includes('lock')) return 'muted';
  return 'neutral';
}

function StatusPill({ tone, children }) {
  return <span className={`status-pill ${tone || 'neutral'}`}>{children}</span>;
}

function IconButton({ icon: Icon, children, kind = 'secondary', busy, ...props }) {
  return (
    <button className={`button ${kind}`} disabled={busy || props.disabled} {...props}>
      {busy ? <Loader2 className="spin" size={16} /> : <Icon size={16} />}
      <span>{children}</span>
    </button>
  );
}

function formatBytes(value) {
  const size = Number(value || 0);
  if (size > 1024 * 1024) return `${(size / 1024 / 1024).toFixed(1)} MB`;
  if (size > 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${size} B`;
}

async function apiGet(path) {
  const res = await fetch(path, { cache: 'no-store' });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `GET ${path} failed`);
  return data;
}

async function apiPost(path, payload = {}) {
  const res = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `POST ${path} failed`);
  return data;
}

function Timeline({ stages }) {
  return (
    <aside className="timeline-panel">
      <div className="panel-title">
        <Gauge size={18} />
        <span>阶段流程</span>
      </div>
      <div className="stage-list">
        {stages.map((stage) => (
          <div key={stage.id} className={`stage-row ${stage.is_current ? 'current' : ''}`}>
            <div className={`stage-dot ${statusTone(stage.status)}`}>
              {stage.is_completed ? <CheckCircle2 size={12} /> : stage.is_locked ? <Lock size={12} /> : <Clock3 size={12} />}
            </div>
            <div className="stage-main">
              <div className="stage-name">{STAGE_LABELS[stage.id] || stage.id}</div>
              <div className="stage-id">{stage.id}</div>
            </div>
            <StatusPill tone={statusTone(stage.status)}>{stage.status}</StatusPill>
          </div>
        ))}
      </div>
    </aside>
  );
}

function ReportCard({ title, report, icon: Icon }) {
  const tone = report?.exists === false ? 'muted' : statusTone(report?.status || (Number(report?.fail_count || 0) ? 'fail' : Number(report?.warn_count || 0) ? 'warn' : 'pass'));
  return (
    <div className="report-tile">
      <div className="report-head">
        <Icon size={17} />
        <span>{title}</span>
      </div>
      <div className="report-metrics">
        <StatusPill tone={tone}>{report?.exists === false ? 'missing' : report?.status || 'ready'}</StatusPill>
        <span>fail {report?.fail_count ?? '-'}</span>
        <span>warn {report?.warn_count ?? '-'}</span>
      </div>
      <div className="report-path">{report?.path || report?.label || 'not available'}</div>
    </div>
  );
}

function CommandCenter({ state, busy, onAction }) {
  const workflow = state?.workflow || {};
  const reports = state?.reports || {};
  const currentStage = workflow.current_stage || '';
  const writable = state?.server?.write_actions_enabled;

  return (
    <section className="command-panel">
      <div className="command-top">
        <div>
          <div className="section-kicker">当前控制点</div>
          <h1>{STAGE_LABELS[currentStage] || currentStage || '未读取状态'}</h1>
          <p>保持 deep_sequential：每次只推进当前阶段，脚本仍由工作流控制器校验。</p>
        </div>
        <StatusPill tone={writable ? 'ok' : 'danger'}>{writable ? '本地可执行' : '写动作禁用'}</StatusPill>
      </div>

      <div className="action-row">
        <IconButton icon={Play} kind="primary" busy={busy} disabled={!currentStage || !writable} onClick={() => onAction('run-current', currentStage)}>
          运行当前阶段
        </IconButton>
        {CHECK_ACTIONS.map((item) => (
          <IconButton key={item.id} icon={item.icon} busy={busy} onClick={() => onAction(item.id)}>
            {item.label}
          </IconButton>
        ))}
      </div>

      <div className="report-grid">
        <ReportCard title="Gate" report={reports.gates} icon={ShieldCheck} />
        <ReportCard title="Contracts" report={reports.contracts} icon={ClipboardCheck} />
        <ReportCard title="Skill Router" report={reports.skill_router} icon={GitBranch} />
        <ReportCard title="Learning" report={reports.learning} icon={Database} />
      </div>
    </section>
  );
}

function GatePanel({ state, busy, onConfirm }) {
  const gate = state?.workflow?.pending_gate;
  const writable = state?.server?.write_actions_enabled;
  return (
    <aside className="gate-panel">
      <div className="panel-title">
        <ShieldCheck size={18} />
        <span>人工闸门</span>
      </div>
      {gate ? (
        <>
          <div className="gate-card active">
            <div className="gate-label">pending_gate</div>
            <div className="gate-name">{gate}</div>
            <p>确认前请查看模型、结果、全文或修订产物。确认动作只调用 `confirm_gate.py`。</p>
          </div>
          <IconButton icon={CheckCircle2} kind="primary" disabled={!writable} busy={busy} onClick={() => onConfirm(gate)}>
            确认闸门
          </IconButton>
        </>
      ) : (
        <div className="gate-card">
          <div className="gate-label">status</div>
          <div className="gate-name">当前无待确认 gate</div>
          <p>阶段完成到硬 gate 后，这里会出现确认入口。</p>
        </div>
      )}
      <div className="safety-list">
        <div><CheckCircle2 size={14} />不提供 stage all</div>
        <div><CheckCircle2 size={14} />不直接编辑合同</div>
        <div><CheckCircle2 size={14} />不自动应用学习建议</div>
      </div>
    </aside>
  );
}

function JobPanel({ jobs, selectedJob, onSelectJob }) {
  const recent = jobs?.recent || [];
  const active = jobs?.active_job_id;
  return (
    <section className="job-panel">
      <div className="panel-title">
        <SquareTerminal size={18} />
        <span>运行日志</span>
        {active && <StatusPill tone="warn">running {active}</StatusPill>}
      </div>
      <div className="job-layout">
        <div className="job-list">
          {recent.length ? recent.map((job) => (
            <button key={job.job_id} className={`job-row ${selectedJob?.job_id === job.job_id ? 'selected' : ''}`} onClick={() => onSelectJob(job)}>
              <span>{job.action}</span>
              <StatusPill tone={statusTone(job.status)}>{job.status}</StatusPill>
            </button>
          )) : <div className="empty-note">还没有通过 Web 控制台运行任务。</div>}
        </div>
        <pre className="log-view">{selectedJob?.log_tail || '选择一个任务查看日志尾部。'}</pre>
      </div>
    </section>
  );
}

function ArtifactBrowser({ groups, activeTab, setActiveTab, selectedFile, setSelectedFile, fileContent, onPreview }) {
  const files = groups?.[activeTab] || [];
  return (
    <section className="artifact-panel">
      <div className="tab-row">
        {TABS.map((tab) => (
          <button key={tab} className={`tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
            {tab}
          </button>
        ))}
      </div>
      <div className="artifact-layout">
        <div className="file-list">
          {files.length ? files.map((file) => (
            <button key={file.path} className={`file-row ${selectedFile?.path === file.path ? 'selected' : ''}`} onClick={() => { setSelectedFile(file); onPreview(file.path); }}>
              <FileText size={15} />
              <span>{file.label}</span>
              <small>{formatBytes(file.size)}</small>
            </button>
          )) : <div className="empty-note">这个分组暂无可预览文件。</div>}
        </div>
        <div className="preview-pane">
          <div className="preview-head">
            <Eye size={16} />
            <span>{selectedFile?.path || '文件预览'}</span>
          </div>
          <pre>{fileContent || '选择左侧文件查看内容。'}</pre>
        </div>
      </div>
    </section>
  );
}

function RunHistory({ runs, selectedRunId, onSelectRun }) {
  return (
    <aside className="sandbox-history-panel">
      <div className="panel-title">
        <History size={18} />
        <span>运行历史</span>
        <small className="panel-count">{runs.length} 条</small>
      </div>
      <div className="sandbox-run-list">
        {runs.length === 0 ? (
          <div className="empty-note">暂无训练记录。</div>
        ) : (
          runs.map((run) => (
            <button
              key={run.run_id}
              className={`sandbox-run-row ${selectedRunId === run.run_id ? 'selected' : ''}`}
              onClick={() => onSelectRun(run.run_id)}
            >
              <div className="sandbox-run-head">
                <StatusPill tone={statusTone(run.status)}>{run.status}</StatusPill>
                <span className="sandbox-run-mode">
                  {run.mode === 'training_sandbox' ? '训练' : '辅助'}
                </span>
              </div>
              <div className="sandbox-run-id">{run.run_id}</div>
              <div className="sandbox-run-created">{run.created_at}</div>
              {run.notes && <div className="sandbox-run-notes">{run.notes}</div>}
            </button>
          ))
        )}
      </div>
    </aside>
  );
}

function ManifestView({ manifest }) {
  const entries = Object.entries(manifest || {}).filter(([k]) => !k.endsWith('_log_tail'));
  if (entries.length === 0) return <pre className="report-content">Manifest 为空。</pre>;
  return (
    <div className="manifest-grid">
      {entries.map(([key, value]) => (
        <div key={key} className="manifest-row">
          <span className="manifest-key">{key}</span>
          <span className="manifest-value">
            {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
          </span>
        </div>
      ))}
    </div>
  );
}

function ValidationView({ validation }) {
  if (!validation || !validation.exists) {
    return <pre className="report-content">验证报告不存在。</pre>;
  }
  return (
    <div className="validation-report">
      <div className="validation-summary">
        <span>状态: <StatusPill tone={statusTone(validation.status)}>{validation.status}</StatusPill></span>
        <span>失败: {validation.fail_count ?? '-'}</span>
        <span>警告: {validation.warn_count ?? '-'}</span>
      </div>
      {validation.issues?.length > 0 && (
        <div className="validation-issues">
          {validation.issues.map((issue, i) => (
            <div key={i} className={`issue-row ${issue.level}`}>
              <StatusPill tone={issue.level === 'fail' ? 'danger' : 'warn'}>{issue.level}</StatusPill>
              <span>{issue.item}: {issue.detail}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function resolveReportPath(tab, runDetail) {
  const reports = runDetail?.reports || {};
  switch (tab) {
    case 'Revision Queue': return reports.revision_queue?.path || null;
    case 'Gap Report': return reports.gap?.path || null;
    case 'Copy Risk': return reports.copy_risk?.path || null;
    case 'Full Gap': return reports.full_gap?.path || null;
    default: return null;
  }
}

function RunDetail({ runDetail, reportContent, activeDetailTab, setActiveDetailTab, onPreviewReport }) {
  if (!runDetail) {
    return (
      <section className="sandbox-detail-panel">
        <div className="empty-state">
          <Eye size={32} />
          <p>选择一个运行查看详情</p>
        </div>
      </section>
    );
  }

  const manifest = runDetail.manifest || {};
  const reports = runDetail.reports || {};

  return (
    <section className="sandbox-detail-panel">
      <div className="panel-title">
        <FileText size={18} />
        <span>{runDetail.run_id}</span>
        <StatusPill tone={statusTone(manifest.status)}>{manifest.status}</StatusPill>
      </div>

      <div className="tab-row">
        {RUN_DETAIL_TABS.map((tab) => (
          <button
            key={tab}
            className={`tab ${activeDetailTab === tab ? 'active' : ''}`}
            onClick={() => {
              setActiveDetailTab(tab);
              const reportPath = resolveReportPath(tab, runDetail);
              if (reportPath) onPreviewReport(reportPath);
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="sandbox-detail-body">
        {activeDetailTab === 'Manifest' && <ManifestView manifest={manifest} />}
        {activeDetailTab === 'Revision Queue' && (
          <pre className="report-content">{reportContent || '暂无修正队列数据。'}</pre>
        )}
        {activeDetailTab === 'Gap Report' && (
          <pre className="report-content">{reportContent || '暂无 gap 报告数据。'}</pre>
        )}
        {activeDetailTab === 'Validation' && (
          <ValidationView validation={reports.validation} />
        )}
        {activeDetailTab === 'Copy Risk' && (
          <pre className="report-content">{reportContent || '暂无 copy risk 数据。'}</pre>
        )}
        {activeDetailTab === 'Full Gap' && (
          <pre className="report-content">{reportContent || '暂无完整 gap 报告。'}</pre>
        )}
      </div>

      <div className="sandbox-run-meta">
        <span>创建: {manifest.created_at || '-'}</span>
        <span>迭代: {manifest.max_iterations || '-'}</span>
        <span>{manifest.mode === 'training_sandbox' ? '训练沙盒' : '正式辅助'}</span>
      </div>
    </section>
  );
}

function SandboxActions({ startForm, onFormChange, onStart, busy, runDetail, onBenchmark, onValidate, runs }) {
  const feedbackRuns = (runs || []).filter((run) => run.mode === 'training_sandbox' && run.status === 'completed');
  return (
    <aside className="sandbox-actions-panel">
      <div className="panel-title">
        <Play size={18} />
        <span>启动沙盒训练</span>
      </div>

      <div className="sandbox-form">
        <div className="form-group">
          <label>运行模式</label>
          <select
            value={startForm.mode}
            onChange={(e) => onFormChange({ ...startForm, mode: e.target.value })}
            disabled={busy}
          >
            <option value="training_sandbox">训练沙盒 (training_sandbox)</option>
            <option value="formal_assist">正式辅助 (formal_assist)</option>
          </select>
        </div>

        {startForm.mode === 'formal_assist' && (
          <div className="form-group">
            <label>训练反馈来源</label>
            <select
              value={startForm.feedbackRunId || ''}
              onChange={(e) => onFormChange({ ...startForm, feedbackRunId: e.target.value })}
              disabled={busy}
            >
              <option value="">自动选择最新通过训练 run</option>
              {feedbackRuns.map((run) => (
                <option key={run.run_id} value={run.run_id}>
                  {run.run_id}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="form-group">
          <label>最大迭代次数</label>
          <input
            type="number"
            min={1}
            max={10}
            value={startForm.maxIterations}
            onChange={(e) => onFormChange({ ...startForm, maxIterations: parseInt(e.target.value) || 3 })}
            disabled={busy || startForm.mode !== 'training_sandbox'}
          />
        </div>

        <div className="form-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={startForm.dryRun}
              onChange={(e) => onFormChange({ ...startForm, dryRun: e.target.checked })}
              disabled={busy}
            />
            <span>Dry Run (仅验证配置，不执行)</span>
          </label>
        </div>

        <IconButton icon={Play} kind="primary" busy={busy} onClick={onStart}>
          启动运行
        </IconButton>
      </div>

      {runDetail && (
        <>
          <div className="panel-title" style={{ marginTop: '18px' }}>
            <ListChecks size={18} />
            <span>运行操作</span>
          </div>
          <div className="action-row">
            <IconButton icon={RefreshCcw} busy={busy} onClick={() => onBenchmark(runDetail.run_id)}>
              重新基准测试
            </IconButton>
            <IconButton icon={ShieldCheck} busy={busy} onClick={() => onValidate(runDetail.run_id)}>
              重新验证
            </IconButton>
          </div>
        </>
      )}
    </aside>
  );
}

function Header({ state, onRefresh, busy, sandboxMode, onToggleMode }) {
  const workflow = state?.workflow || {};
  return (
    <header className="app-header">
      <div className="brand-lockup">
        <div className="brand-mark"><Activity size={20} /></div>
        <div>
          <div className="brand-title">Math Workflow Console</div>
          <div className="brand-subtitle">v3.2 MVP · 本地控制台</div>
        </div>
      </div>
      <div className="header-status">
        <button
          className={`mode-toggle ${sandboxMode ? 'sandbox' : 'formal'}`}
          onClick={onToggleMode}
          title={sandboxMode ? '切换到正式流水线' : '切换到沙盒训练'}
        >
          {sandboxMode ? <FlaskConical size={16} /> : <Activity size={16} />}
          <span>{sandboxMode ? '沙盒训练' : '正式流水线'}</span>
        </button>
        {!sandboxMode && (
          <>
            <StatusPill tone={workflow.execution_mode === 'deep_sequential' ? 'ok' : 'danger'}>{workflow.execution_mode || 'unknown'}</StatusPill>
            <StatusPill tone={workflow.allow_parallel ? 'danger' : 'ok'}>{workflow.allow_parallel ? 'parallel on' : 'parallel off'}</StatusPill>
          </>
        )}
        <IconButton icon={RefreshCcw} busy={busy} onClick={onRefresh}>刷新</IconButton>
      </div>
    </header>
  );
}

function App() {
  const [state, setState] = useState(null);
  const [artifacts, setArtifacts] = useState({});
  const [activeTab, setActiveTab] = useState('Contracts');
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [selectedJob, setSelectedJob] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const [sandboxMode, setSandboxMode] = useState(false);
  const [sandboxRuns, setSandboxRuns] = useState([]);
  const [selectedRunId, setSelectedRunId] = useState(null);
  const [runDetail, setRunDetail] = useState(null);
  const [activeDetailTab, setActiveDetailTab] = useState('Manifest');
  const [startForm, setStartForm] = useState({ mode: 'training_sandbox', maxIterations: 3, dryRun: false, feedbackRunId: '' });

  const loadAll = useCallback(async () => {
    setError('');
    const [stateData, artifactData] = await Promise.all([apiGet('/api/state'), apiGet('/api/artifacts')]);
    setState(stateData);
    setArtifacts(artifactData.groups || {});
    if (selectedJob?.job_id) {
      const jobData = await apiGet(`/api/jobs/${selectedJob.job_id}`);
      setSelectedJob(jobData.job);
    }
  }, [selectedJob?.job_id]);

  const loadSandboxRuns = useCallback(async () => {
    setError('');
    const [stateData, data] = await Promise.all([apiGet('/api/state'), apiGet('/api/sandbox/runs')]);
    setState(stateData);
    setSandboxRuns(data.runs || []);
    const feedbackOptions = (data.runs || []).filter((run) => run.mode === 'training_sandbox' && run.status === 'completed');
    setStartForm((prev) => (prev.feedbackRunId || feedbackOptions.length === 0 ? prev : { ...prev, feedbackRunId: feedbackOptions[0].run_id }));
    if (selectedJob?.job_id) {
      const jobData = await apiGet(`/api/jobs/${selectedJob.job_id}`);
      setSelectedJob(jobData.job);
    }
  }, [selectedJob?.job_id]);

  const loadRunDetail = useCallback(async (runId) => {
    if (!runId) { setRunDetail(null); return; }
    const data = await apiGet(`/api/sandbox/runs/${runId}`);
    setRunDetail(data);
  }, []);

  useEffect(() => {
    if (sandboxMode) {
      loadSandboxRuns().catch((err) => setError(err.message));
    } else {
      loadAll().catch((err) => setError(err.message));
    }
  }, [sandboxMode, loadAll, loadSandboxRuns]);

  useEffect(() => {
    const timer = setInterval(() => {
      if (sandboxMode) {
        loadSandboxRuns().catch(() => {});
      } else {
        loadAll().catch(() => {});
      }
    }, 4000);
    return () => clearInterval(timer);
  }, [sandboxMode, loadAll, loadSandboxRuns]);

  const activeJob = useMemo(() => {
    const activeId = state?.jobs?.active_job_id;
    return (state?.jobs?.recent || []).find((job) => job.job_id === activeId);
  }, [state]);

  async function handleAction(action, expectedText = '') {
    const mutating = action === 'run-current';
    let payload = {};
    if (mutating) {
      const confirmation = window.prompt(`输入 ${expectedText} 确认运行当前阶段`);
      if (confirmation !== expectedText) return;
      payload = { confirmation };
    }
    setBusy(true);
    setError('');
    try {
      const endpoint = action === 'run-current' ? '/api/actions/run-current' : `/api/actions/${action}`;
      const res = await apiPost(endpoint, payload);
      setSelectedJob(res.job);
      await loadAll();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleGateConfirm(gate) {
    const confirmation = window.prompt(`输入 ${gate} 确认人工闸门`);
    if (confirmation !== gate) return;
    setBusy(true);
    setError('');
    try {
      const res = await apiPost('/api/actions/confirm-gate', { confirmation });
      setSelectedJob(res.job);
      await loadAll();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function previewFile(path) {
    setError('');
    setFileContent('读取中...');
    try {
      const data = await apiGet(`/api/file?path=${encodeURIComponent(path)}`);
      setFileContent(data.text);
    } catch (err) {
      setFileContent('');
      setError(err.message);
    }
  }

  async function selectJob(job) {
    setSelectedJob(job);
    try {
      const data = await apiGet(`/api/jobs/${job.job_id}`);
      setSelectedJob(data.job);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleSandboxStart() {
    setBusy(true);
    setError('');
    try {
      const res = await apiPost('/api/sandbox/start', {
        mode: startForm.mode,
        max_iterations: startForm.maxIterations,
        dry_run: startForm.dryRun,
        feedback_run_id: startForm.mode === 'formal_assist' ? startForm.feedbackRunId : '',
      });
      setSelectedJob(res.job);
      await loadSandboxRuns();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleSandboxBenchmark(runId) {
    setBusy(true);
    setError('');
    try {
      const res = await apiPost(`/api/sandbox/benchmark/${runId}`);
      setSelectedJob(res.job);
      await loadSandboxRuns();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleSandboxValidate(runId) {
    setBusy(true);
    setError('');
    try {
      const res = await apiPost(`/api/sandbox/validate/${runId}`);
      setSelectedJob(res.job);
      await loadSandboxRuns();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const stages = state?.workflow?.stages || [];

  return (
    <div className="app-shell">
      <Header
        state={state}
        onRefresh={() => (sandboxMode
          ? loadSandboxRuns().catch((err) => setError(err.message)).then(() => { if (selectedRunId) loadRunDetail(selectedRunId); })
          : loadAll().catch((err) => setError(err.message))
        )}
        busy={busy}
        sandboxMode={sandboxMode}
        onToggleMode={() => {
          setSandboxMode((prev) => !prev);
          setSelectedRunId(null);
          setRunDetail(null);
        }}
      />
      {error && (
        <div className="error-banner">
          <AlertTriangle size={16} />
          <span>{error}</span>
        </div>
      )}
      {sandboxMode ? (
        <main className="sandbox-grid">
          <RunHistory
            runs={sandboxRuns}
            selectedRunId={selectedRunId}
            onSelectRun={(runId) => {
              setSelectedRunId(runId);
              setActiveDetailTab('Manifest');
              setFileContent('');
              loadRunDetail(runId).catch((err) => setError(err.message));
            }}
          />
          <RunDetail
            runDetail={runDetail}
            reportContent={fileContent}
            activeDetailTab={activeDetailTab}
            setActiveDetailTab={setActiveDetailTab}
            onPreviewReport={previewFile}
          />
          <SandboxActions
            startForm={startForm}
            onFormChange={setStartForm}
            onStart={handleSandboxStart}
            busy={busy || Boolean(activeJob)}
            runDetail={runDetail}
            onBenchmark={handleSandboxBenchmark}
            onValidate={handleSandboxValidate}
            runs={sandboxRuns}
          />
          <JobPanel jobs={state?.jobs} selectedJob={selectedJob} onSelectJob={selectJob} />
        </main>
      ) : (
        <main className="dashboard-grid">
          <Timeline stages={stages} />
          <div className="main-stack">
            <CommandCenter state={state} busy={busy || Boolean(activeJob)} onAction={handleAction} />
            <ArtifactBrowser
              groups={artifacts}
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              selectedFile={selectedFile}
              setSelectedFile={setSelectedFile}
              fileContent={fileContent}
              onPreview={previewFile}
            />
          </div>
          <div className="side-stack">
            <GatePanel state={state} busy={busy || Boolean(activeJob)} onConfirm={handleGateConfirm} />
            <JobPanel jobs={state?.jobs} selectedJob={selectedJob} onSelectJob={selectJob} />
          </div>
        </main>
      )}
      <footer className="app-footer">
        <BookOpen size={14} />
        <span>所有动作通过现有脚本执行；Web 控制台不直接编辑合同、论文或 workflow_state。</span>
        <ChevronRight size={14} />
        <span>{state?.generated_at || 'loading'}</span>
      </footer>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
