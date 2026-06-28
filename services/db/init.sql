-- ==========================================
-- Create ENUM for job status
-- ==========================================
CREATE TYPE job_status AS ENUM (
    'pending',
    'processing',
    'completed',
    'failed'
);

-- ==========================================
-- Jobs table
-- ==========================================
CREATE TABLE jobs (
    job_id                  UUID PRIMARY KEY,
    status                  job_status NOT NULL DEFAULT 'pending',
    original_s3_key         TEXT NOT NULL,
    results                 JSONB,
    error_message           TEXT,
    retry_count             INTEGER NOT NULL DEFAULT 0,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    processing_started_at   TIMESTAMPTZ,
    completed_at            TIMESTAMPTZ,
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -- ==========================================
-- -- Indexes
-- -- ==========================================
-- CREATE INDEX idx_jobs_status
-- ON jobs(status);