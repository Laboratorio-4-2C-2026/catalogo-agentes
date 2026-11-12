-- Tablas del agente g16-eureka-aura-manager.
-- Modelo de libro mayor: el aura de cada persona es la suma de sus movimientos.
-- Nunca se edita ni se borra un movimiento; un error se corrige con un movimiento compensatorio.
-- Idempotente: se puede correr más de una vez.

create table if not exists public.aura_members (
  github text primary key,
  nombre text not null,
  apodo text not null unique,
  activo boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.aura_ledger (
  id bigint generated always as identity primary key,
  github text not null references public.aura_members(github),
  delta int not null check (delta between -50 and 50 and delta <> 0),
  categoria text not null check (categoria in (
    'entrega', 'calidad', 'proceso', 'colaboracion', 'comunicacion', 'incidente', 'correccion'
  )),
  motivo text not null check (length(motivo) between 10 and 500),
  evidencia text,
  corrige_id bigint references public.aura_ledger(id),
  registrado_por text not null default 'g16-eureka-aura-manager',
  created_at timestamptz not null default now()
);

create index if not exists aura_ledger_github_idx on public.aura_ledger (github, created_at desc);

-- Movimientos inmutables: sin UPDATE ni DELETE, ni siquiera para el service_role vía trigger.
create or replace function public.aura_ledger_inmutable()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  raise exception 'aura_ledger es solo de inserción: corregí con un movimiento de categoria correccion'
    using errcode = 'P0001';
end;
$$;

drop trigger if exists trg_aura_ledger_inmutable on public.aura_ledger;
create trigger trg_aura_ledger_inmutable
before update or delete on public.aura_ledger
for each row execute function public.aura_ledger_inmutable();

create or replace view public.aura_scores
with (security_invoker = true) as
select
  m.github,
  m.nombre,
  m.apodo,
  coalesce(sum(l.delta), 0)::int as aura,
  count(l.id)::int as movimientos,
  max(l.created_at) as ultimo_movimiento
from public.aura_members m
left join public.aura_ledger l on l.github = m.github
where m.activo
group by m.github, m.nombre, m.apodo;

-- RLS habilitado y sin policies: el navegador (anon/authenticated) no ve ni toca nada.
-- Solo se accede por MCP / service_role.
alter table public.aura_members enable row level security;
alter table public.aura_ledger enable row level security;

insert into public.aura_members (github, nombre, apodo) values
  ('LedesmaNicolas', 'Nicolás Ledesma', 'nico'),
  ('bautista237', 'Bautista', 'bauti')
on conflict (github) do nothing;
