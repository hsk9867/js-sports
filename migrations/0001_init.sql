-- JS스포츠 관리자: 덮어쓴 콘텐츠 + 업로드 사진 + 방문 기록 + 상담 신청
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS media (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data TEXT NOT NULL,
  size INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS hits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL, day TEXT NOT NULL, hour INTEGER NOT NULL,
  type TEXT NOT NULL, name TEXT, path TEXT NOT NULL,
  ref_host TEXT, ref_url TEXT, source TEXT NOT NULL, medium TEXT, campaign TEXT,
  device TEXT, browser TEXT, os TEXT, country TEXT, city TEXT,
  vid TEXT NOT NULL, screen TEXT, lang TEXT
);
CREATE INDEX IF NOT EXISTS idx_hits_day ON hits(day, type);
CREATE INDEX IF NOT EXISTS idx_hits_ts ON hits(ts);
CREATE TABLE IF NOT EXISTS inquiries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL, day_kst TEXT NOT NULL,
  name TEXT NOT NULL, tel TEXT NOT NULL, type TEXT, msg TEXT,
  page TEXT, ua TEXT, status TEXT NOT NULL DEFAULT 'new', memo TEXT
);
CREATE INDEX IF NOT EXISTS idx_inq_ts ON inquiries(ts);
