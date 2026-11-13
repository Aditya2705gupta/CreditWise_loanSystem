-- CreditWise schema. Paste into Supabase -> SQL Editor -> Run.

-- 1. Historical training data (the project's loan_approval_data.csv)
create table if not exists public.loan_applications (
  id                 bigint generated always as identity primary key,
  applicant_id       integer,
  applicant_income   numeric,
  coapplicant_income numeric,
  employment_status  text,
  age                numeric,
  marital_status     text,
  dependents         numeric,
  credit_score       numeric,
  existing_loans     numeric,
  dti_ratio          numeric,
  savings            numeric,
  collateral_value   numeric,
  loan_amount        numeric,
  loan_term          numeric,
  loan_purpose       text,
  property_area      text,
  education_level    text,
  gender             text,
  employer_category  text,
  loan_approved      text check (loan_approved in ('Yes', 'No'))
);

-- 2. Every check made on the website
create table if not exists public.predictions (
  id                 bigint generated always as identity primary key,
  created_at         timestamptz not null default now(),
  applicant_income   numeric,
  coapplicant_income numeric,
  employment_status  text,
  age                numeric,
  marital_status     text,
  dependents         numeric,
  credit_score       numeric,
  existing_loans     numeric,
  dti_ratio          numeric,
  savings            numeric,
  collateral_value   numeric,
  loan_amount        numeric,
  loan_term          numeric,
  loan_purpose       text,
  property_area      text,
  education_level    text,
  gender             text,
  employer_category  text,
  predicted_approved boolean not null,
  approval_probability numeric not null,
  model_name         text,
  model_version      text
);

-- 3. Training runs and their test metrics
create table if not exists public.model_runs (
  id               bigint generated always as identity primary key,
  created_at       timestamptz not null default now(),
  version          text not null,
  model_name       text not null,
  is_selected      boolean not null default false,
  data_source      text,
  n_rows           integer,
  accuracy         numeric,
  precision        numeric,
  recall           numeric,
  f1               numeric,
  confusion_matrix jsonb
);

-- Security: Row Level Security on every table.
-- The service-role key (used only by local scripts) bypasses RLS.
-- The public website uses the anon key and may ONLY insert predictions; it cannot read anything.
alter table public.loan_applications enable row level security;
alter table public.predictions       enable row level security;
alter table public.model_runs        enable row level security;

drop policy if exists "website can insert predictions" on public.predictions;
create policy "website can insert predictions" on public.predictions
  for insert to anon with check (true);
