export type Severity = "critical" | "high" | "medium" | "low" | "info";

export type ScanStatus = "pending" | "queued" | "running" | "completed" | "failed" | "cancelled";

export type AlertStatus = "new" | "acknowledged" | "investigating" | "resolved" | "false_positive";

export type SubmissionStatus =
  | "submitted"
  | "triaging"
  | "accepted"
  | "duplicate"
  | "rejected"
  | "fixed"
  | "paid";

export type UserRole =
  | "admin"
  | "ciso"
  | "cto"
  | "manager"
  | "engineer"
  | "hunter"
  | "analyst"
  | "auditor";

export type ScanType = "web" | "api" | "network" | "full";

export type ScanLevel = "fast" | "medium" | "deep";

export type Tier = "starter" | "pro" | "enterprise";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  tenant_id: string;
  created_at: string;
  last_login?: string;
  avatar_url?: string;
}

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  tier: Tier;
  created_at: string;
  user_count: number;
  active: boolean;
}

export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in?: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface Scan {
  id: string;
  target: string;
  scan_type: ScanType;
  scan_level: ScanLevel;
  tier: Tier;
  status: ScanStatus;
  progress: number;
  findings_count: number;
  started_at: string;
  completed_at?: string;
  duration_seconds?: number;
  created_by: string;
  tenant_id: string;
  raw_output?: string;
}

export interface Vulnerability {
  id: string;
  scan_id?: string;
  title: string;
  description: string;
  severity: Severity;
  cvss_score: number;
  cvss_vector?: string;
  cwe?: string;
  cve?: string;
  affected_url?: string;
  affected_param?: string;
  proof_of_concept?: string;
  remediation: string;
  references?: string[];
  status: "open" | "confirmed" | "fixed" | "wontfix" | "duplicate";
  discovered_at: string;
  fixed_at?: string;
}

export interface Alert {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  source: string;
  status: AlertStatus;
  category: string;
  asset?: string;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  assigned_to?: string;
  raw_event?: Record<string, unknown>;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  status: "open" | "containment" | "eradication" | "recovery" | "closed";
  detected_at: string;
  closed_at?: string;
  assigned_to?: string;
  alerts: Alert[];
  timeline: IncidentEvent[];
}

export interface IncidentEvent {
  id: string;
  incident_id: string;
  type: string;
  description: string;
  user: string;
  timestamp: string;
}

export interface BugBountyProgram {
  id: string;
  name: string;
  description: string;
  active: boolean;
  scope: string[];
  out_of_scope: string[];
  reward_critical: number;
  reward_high: number;
  reward_medium: number;
  reward_low: number;
  total_payout: number;
  total_submissions: number;
  total_paid: number;
  triaged_count: number;
  created_at: string;
}

export interface Submission {
  id: string;
  program_id: string;
  hunter_id: string;
  hunter_name: string;
  title: string;
  description: string;
  severity: Severity;
  status: SubmissionStatus;
  cvss_score: number;
  cvss_vector?: string;
  affected_url: string;
  proof_of_concept: string;
  remediation?: string;
  reward_amount?: number;
  paid_at?: string;
  submitted_at: string;
  triaged_at?: string;
  resolved_at?: string;
}

export interface ReconResult {
  id: string;
  target: string;
  type: "subdomain" | "port" | "service" | "technology" | "endpoint" | "credential";
  value: string;
  metadata: Record<string, unknown>;
  discovered_at: string;
}

export interface Exploit {
  id: string;
  target: string;
  cve?: string;
  technique: string;
  kill_chain_phase:
    | "reconnaissance"
    | "weaponization"
    | "delivery"
    | "exploitation"
    | "installation"
    | "command_control"
    | "actions";
  status: "planned" | "running" | "successful" | "failed" | "detected";
  evidence?: string;
  started_at: string;
  completed_at?: string;
}

export interface ThreatIntel {
  id: string;
  source: string;
  ioc_type: "ip" | "domain" | "hash" | "url" | "email";
  ioc_value: string;
  threat_type: string;
  confidence: number;
  first_seen: string;
  last_seen: string;
  tags: string[];
}

export interface LogEntry {
  id: string;
  timestamp: string;
  source: string;
  level: "debug" | "info" | "warn" | "error" | "critical";
  message: string;
  fields: Record<string, unknown>;
}

export interface ScheduledJob {
  id: string;
  name: string;
  job_type: "scan" | "report" | "recon" | "intel_pull";
  cron: string;
  target?: string;
  next_run: string;
  last_run?: string;
  enabled: boolean;
  created_at: string;
}

export interface Report {
  id: string;
  title: string;
  role: "ciso" | "cto" | "manager" | "engineer" | "board" | "compliance";
  generated_at: string;
  generated_by: string;
  scan_id?: string;
  format: "html" | "pdf" | "json";
  download_url: string;
  size_bytes: number;
}

export interface Invoice {
  id: string;
  tenant_id: string;
  amount: number;
  currency: string;
  status: "draft" | "sent" | "paid" | "overdue" | "void";
  issued_at: string;
  due_at: string;
  paid_at?: string;
  line_items: InvoiceLineItem[];
}

export interface InvoiceLineItem {
  description: string;
  quantity: number;
  unit_price: number;
  total: number;
}

export interface TrainingTrack {
  code: string;
  name: string;
  description: string;
  category: "bug_bounty" | "red_team" | "blue_team";
  modules: TrainingModule[];
  progress: number;
}

export interface TrainingModule {
  code: string;
  name: string;
  level: "L0" | "L1" | "L2" | "L3" | "L4";
  duration_hours: number;
  topics: string[];
  labs: TrainingLab[];
  completed: boolean;
  progress: number;
}

export interface TrainingLab {
  id: string;
  name: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
  estimated_minutes: number;
  completed: boolean;
}

export interface Asset {
  id: string;
  type: "domain" | "ip" | "iot" | "cctv" | "endpoint";
  name: string;
  value: string;
  criticality: "low" | "medium" | "high" | "critical";
  tags: string[];
  metadata: Record<string, unknown>;
  last_scanned?: string;
  created_at: string;
}

export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface DashboardStats {
  active_scans: number;
  open_vulnerabilities: number;
  critical_alerts: number;
  monthly_revenue: number;
  vulnerability_trend: { date: string; critical: number; high: number; medium: number; low: number }[];
  scan_activity: { date: string; count: number }[];
  recent_alerts: Alert[];
  recent_submissions: Submission[];
}
